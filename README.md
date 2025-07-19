# tg2signal-stickers

> Миграция стикерпаков из Telegram в Signal, чтобы ваши любимые стикеры были с вами.

> ‼️ ВНИМАНИЕ: не используйте скрипт на основном аккаунте Telegram, так как есть риск блокировки или выхода со всех устройств. Лучше создайте или купите другой аккаунт который не жалко в случае чего, он понадобится только на момент загрузки стикеров и не более.

> ❗ Анимированные стикеры не поддерживаются

## 📖 Описание

Этот скрипт берёт указанный `short_name` набора стикеров из Telegram, скачивает все `.webp`-стикеры и заливает их в ваш Signal-аккаунт. Анимированные TGS-стикеры пока не поддерживаются.

## ⚙️ Требования

- Python ≥ 3.8
- Активный Telegram-аккаунт
- Установленный Signal Desktop

## 🚀 Установка

1. Клонируем репозиторий:

   ```bash
   git clone https://github.com/just-mn/tg2signal-stickers.git
   cd tg2signal-stickers
   ```

2. Создаём виртуальное окружение и активируем его:

   ```bash
   python -m venv .venv
   ```

   для bash/zsh

   ```bash
   source .venv/bin/activate
   ```

   для PowerShell

   ```powershell
   .\.venv\Scripts\activate
   ```

3. Устанавливаем зависимости:

   ```bash
   pip install -r requirements.txt
   ```

## 🔑 Получение учётных данных

### 1. Telegram

1. Заходим на [https://my.telegram.org](https://my.telegram.org) → API Development → Create new application.
2. Куда нибудь сохроняем **API ID** и **API HASH**.

### 2. Signal

Чтобы достать `SIGNAL_USERNAME` и `SIGNAL_PASSWORD`, придётся немного порыться в dev-tools Signal Desktop:

1. Запустите Signal Desktop с флагом `--enable-dev-tools`:
2. Откройте **Developer Tools** (обычно `Ctrl+Shift+I` или через меню).
3. В правом верхнем углу поменяйте JS-контекст с “top” на **Electron Isolated Context**.
4. Перейдите на вкладку **Console** и выполните:

   - это будет ваш SIGNAL_USERNAME
     ```js
     window.reduxStore.getState().items.uuid_id;
     ```
   - это будет ваш SIGNAL_PASSWORD
     ```js
     window.reduxStore.getState().items.password;
     ```

5. Скопируйте оба значения и сохраните.

## 🔧 Конфигурация

Скрипт читает переменные окружения из файла `.env`. Переименуйте `.env.example` в `.env` и заполните его своими данными

## ▶️ Использование

```bash
# Перед запуском убедитесь, что все ENV переменные установлены!
python main.py <short_name>
```

Если не передали `short_name`, скрипт спросит его интерактивно:

```bash
$ python main.py
Enter short_name of the Telegram sticker pack: awesome_pack
```

### Пример

```bash
python main.py funny_animals
```

- Скрипт скачает все `.webp`-стикеры из набора `funny_animals`.
- Игнорирует `.tgs`.
- Соберёт и зальёт набор в Signal.
- В конце выведет ссылку типа:
  ```
  https://signal.art/addstickers/#pack_id=XYZ&pack_key=ABC
  ```
- Все готово. Вы прекрасны ☀️
