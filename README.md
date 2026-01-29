# Административная ПК‑программа (Python + PyQt5)

## Требования
- Python 3.11+

## Установка
1. Создайте виртуальное окружение.
2. Установите зависимости:
   - `pip install -r requirements.txt`
3. Скопируйте `.env.example` в `.env` и задайте `APP_SECRET_KEY`.
   - Для генерации ключа Fernet: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`

## Инициализация базы
- `python -m src.db.init_db`

## Запуск
- `python -m src.app`

## По умолчанию
- Логин: admin
- Пароль: admin123

## Авто‑обновление через GitHub Releases
Приложение проверяет наличие новой версии на старте через:
`https://api.github.com/repos/beu2772hwha/yuniadmin/releases/latest`

Требования к релизу:
- Tag: `vX.Y.Z`
- В Assets должен быть zip‑архив исходников приложения (с папкой `src`).

При наличии новой версии приложение автоматически скачает архив, обновит файлы и перезапустится.
