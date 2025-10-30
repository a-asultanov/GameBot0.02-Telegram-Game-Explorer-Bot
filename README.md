# GameBot0.02 — Telegram Game Explorer

**GameBot0.02** — это асинхронный Telegram-бот на **aiogram 3.x**,  
который позволяет искать и просматривать игры по жанрам, платформам и годам.  
Бот использует собственный Flask API, обращающийся к открытому [RAWG.io API](https://rawg.io/apidocs),  
и поддерживает интерактивное управление через inline-клавиатуры.

---

## Возможности

- Поиск игр по жанру, платформе, году, рейтингу и популярности  
- Подключение к RAWG API через собственный Flask API  
- Просмотр описаний, рейтингов и ссылок на страницы игр  
- Асинхронные запросы через `aiohttp`  
- Кэширование результатов  
- Админка на Flask-Admin с логированием действий пользователей  
- Подключение к базе данных PostgreSQL

---

## Технологии

| Компонент | Используется для |
|------------|------------------|
| Python 3.11+ | Основной язык |
| aiogram 3.22 | Telegram-бот |
| aiohttp | Асинхронные запросы к API |
| Flask + Flask-Admin | Веб-админка и API |
| SQLAlchemy | ORM и модели |
| psycopg2-binary | Подключение к PostgreSQL |
| python-dotenv | Работа с `.env` переменными |

---

## Установка и запуск

```bash
# 1. Клонируем репозиторий
git clone https://github.com/a-asultanov/GameBot0.02-Telegram-Game-Explorer-Bot.git
cd GameBot0.02

# 2. Устанавливаем зависимости
pip install -r requirements.txt

# 3. Создаём файл .env
touch .env


Пример содержимого .env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_telegram_user_id
RAWG_API_KEY=your_rawg_api_key

DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY=your_secret_key




---

## English

**GameBot0.02** is an asynchronous Telegram bot built with **aiogram 3.x** and **Flask API**.  
It allows users to explore games by genre, platform, and release year using the [RAWG.io API](https://rawg.io/apidocs).  
Includes an admin panel built with Flask-Admin and PostgreSQL logging.

### Features
- Search games by genre, platform, and release year  
- Fetch data through a Flask API connected to RAWG.io  
- Asynchronous requests using aiohttp  
- Admin dashboard (Flask-Admin + PostgreSQL)  
- Caching and user activity logging

### Stack
Python 3.11, aiogram 3.22, Flask, Flask-Admin, SQLAlchemy, PostgreSQL, aiohttp
