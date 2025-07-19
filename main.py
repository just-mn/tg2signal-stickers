import os
import anyio
from telethon import TelegramClient, types, functions
from signalstickers_client import StickersClient
from signalstickers_client.models import LocalStickerPack, Sticker
import argparse
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.environ.get("TG_API_ID"))
api_hash = os.environ.get("TG_API_HASH")
signal_user = os.environ.get("SIGNAL_USERNAME")
signal_pass = os.environ.get("SIGNAL_PASSWORD")
download_dir = "./tmp"

if not api_id or not api_hash or not signal_user or not signal_pass:
    raise ValueError(
        "Please set TG_API_ID, TG_API_HASH, SIGNAL_USERNAME, and SIGNAL_PASSWORD in your environment variables."
    )


async def main(sticker_set_short_name: str):
    os.makedirs(download_dir, exist_ok=True)
    mapping = {}

    client = TelegramClient("tgsession", api_id, api_hash)
    await client.start()

    print("🔌 Getting sticker set info...")
    all_sets = await client(functions.messages.GetAllStickersRequest(hash=0))
    target_set = next(
        (s for s in all_sets.sets if s.short_name == sticker_set_short_name), None
    )

    if not target_set:
        print("❌ Sticker pack not found.")
        return

    res = await client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetID(
                id=target_set.id, access_hash=target_set.access_hash
            ),
            hash=0,
        )
    )

    emoji_map = {}
    for pack in res.packs:
        for doc_id in pack.documents:
            emoji_map[doc_id] = pack.emoticon

    print(f"📦 Downloading {len(res.documents)} stickers...")

    for i, doc in enumerate(res.documents):
        ext = ".tgs" if doc.mime_type == "application/x-tgsticker" else ".webp"
        src_path = os.path.join(download_dir, f"{doc.id}{ext}")
        await client.download_media(doc, file=src_path)

        emoji = emoji_map.get(doc.id, "☀️")

        if ext == ".tgs":
            print("❌ TGS stickers are not supported yet. Skipping...")
        else:
            mapping[src_path] = emoji

    await client.disconnect()

    pack = LocalStickerPack()
    pack.title = f"{sticker_set_short_name}"
    pack.author = "3x64"

    for idx, (path, emoji) in enumerate(mapping.items()):
        st = Sticker()
        st.id = idx
        st.emoji = emoji
        with open(path, "rb") as f:
            st.image_data = f.read()
        pack._addsticker(st)

    first_path = next(iter(mapping))
    cover = Sticker()
    cover.id = 0
    with open(first_path, "rb") as f:
        cover.image_data = f.read()
    pack.cover = cover

    print("🚀 Uploading to Signal...")
    async with StickersClient(signal_user, signal_pass) as sc:
        pack_id, pack_key = await sc.upload_pack(pack)

    print(f"🎉 Done! {len(mapping)} stickers uploaded. Add the sticker pack to Signal:")
    print(f"https://signal.art/addstickers/#pack_id={pack_id}&pack_key={pack_key}")
    os.remove(download_dir)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Telegram sticker pack to Signal uploader"
    )
    parser.add_argument(
        "short_name", nargs="?", help="Short name of the Telegram sticker pack"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not args.short_name:
        args.short_name = input(
            "Enter short_name of the Telegram sticker pack: "
        ).strip()
    anyio.run(main, args.short_name)
