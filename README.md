# tg2signal-stickers

> Migrate sticker packs from Telegram to Signal, so your favorite stickers are always with you.

> ‼️ WARNING: Do **not** use this script with your main Telegram account — it may lead to account bans or being logged out from all devices. It's better to create a throwaway account just for the sticker migration process.

> ❗ Animated stickers are **not** supported.

> 🇷🇺 [Read this README in Russian](./README_ru.md)

## 📖 Description

This script takes the `short_name` of a Telegram sticker pack, downloads all the `.webp` stickers, and uploads them to your Signal account.
Animated TGS stickers are not supported at this time.

## ⚙️ Requirements

* Python ≥ 3.8
* An active Telegram account
* Installed Signal Desktop

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/just-mn/tg2signal-stickers.git
   cd tg2signal-stickers
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   For bash/zsh:

   ```bash
   source .venv/bin/activate
   ```

   For PowerShell:

   ```powershell
   .\.venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## 🔑 Getting Credentials

### 1. Telegram

1. Go to [https://my.telegram.org](https://my.telegram.org) → API Development → Create new application
2. Save your **API ID** and **API HASH** somewhere safe.

### 2. Signal

To get your `SIGNAL_USERNAME` and `SIGNAL_PASSWORD`, you'll need to poke around in Signal Desktop's dev tools:

1. Launch Signal Desktop with the `--enable-dev-tools` flag

2. Open **Developer Tools** (usually `Ctrl+Shift+I` or via the menu)

3. Go to the **Console** tab and in the top-right context dropdown, switch from "top" to **Electron Isolated Context**. Then run:

   * Your `SIGNAL_USERNAME`:

     ```js
     window.reduxStore.getState().items.uuid_id;
     ```

   * Your `SIGNAL_PASSWORD`:

     ```js
     window.reduxStore.getState().items.password;
     ```

4. Copy and save both values.

## 🔧 Configuration

The script reads environment variables from a `.env` file.
Rename `.env.example` to `.env` and fill in your credentials.

## ▶️ Usage

```bash
# Make sure all ENV variables are set before running!
python main.py <short_name>
```

If you don’t pass `<short_name>`, the script will ask for it interactively:

```bash
$ python main.py
Enter short_name of the Telegram sticker pack: awesome_pack
```

### Example

```bash
python main.py funny_animals
```

* Downloads all `.webp` stickers from `funny_animals` pack
* Ignores `.tgs` files
* Builds the pack and uploads it to Signal
* Outputs a link like:

  ```
  https://signal.art/addstickers/#pack_id=XYZ&pack_key=ABC
  ```
* Done. You’re awesome ☀️