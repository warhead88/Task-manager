# 🚀 LibreNET Task Manager Bot

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Aiogram](https://img.shields.io/badge/Aiogram-3.22.0-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.43-red.svg)
![Alembic](https://img.shields.io/badge/Alembic-1.14.1-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)

Современный и удобный Telegram-бот для управления задачами. Поддерживает создание, удаление, вывод списков, статистику, а также **гибкую систему напоминаний** с помощью фонового планировщика.

---

## ✨ Возможности

- 📋 **Управление задачами** (Добавление, удаление, просмотр).
- 🌍 **Часовые пояса** (Возможность настроить локальное время).
- 🏆 **Статистика** (Отслеживание выполненных и удаленных задач).
- ⏰ **Система напоминаний** (Единожды, каждый день, по будням, по выходным, еженедельно).
- 🛠 **Архитектура** на основе `src/` с использованием `aiogram 3.x`, `SQLAlchemy v2` и `APScheduler`.
- 📦 **Docker и Docker Compose** "из коробки" вместе с PostgreSQL.
- 🔄 **Миграции базы данных** через Alembic.

---

## 🏗 Архитектура проекта

Проект использует современную структуру директорий:

```text
Task-manager/
├── src/
│   ├── handlers/      # Обработчики команд бота (/remind, /add, /list, и т.д.)
│   ├── middlewares/   # Промежуточный слой (например, регистрация пользователей)
│   ├── bot.py         # Главный файл запуска бота
│   ├── config.py      # Настройки и переменные окружения
│   ├── db.py          # Подключение к БД и сессии
│   ├── scheduler.py   # Фоновые задачи (напоминания APScheduler)
│   └── tables.py      # Модели SQLAlchemy
├── migrations/        # Миграции базы данных Alembic
├── tests/             # Директория для будущих тестов
├── .env               # Файл с секретами (игнорируется в git)
├── docker-compose.yml # Описание контейнеров (Бот + PostgreSQL)
├── Dockerfile         # Сборка образа бота
├── pyproject.toml     # Зависимости и метаданные проекта
└── alembic.ini        # Конфигурация Alembic
```

---

## 🚀 Установка и запуск

### С помощью Docker (Рекомендуется)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/warhead88/Task-manager.git
   cd Task-manager
   ```

2. Настройте переменные окружения:
   Скопируйте пример файла в рабочую версию:
   ```bash
   cp .env.example .env
   ```
   Откройте `.env` и вставьте ваш `BOT_TOKEN` от [@BotFather](https://t.me/botfather). При использовании Docker, `DATABASE_URL` менять не нужно.

3. Соберите и запустите контейнеры:
   ```bash
   docker compose up -d --build
   ```

4. Примените миграции базы данных внутри контейнера бота:
   ```bash
   docker compose exec bot alembic upgrade head
   ```

Бот готов к работе! 🎉

---

## 🔧 Работа с миграциями (Alembic)

Вся структура БД управляется через Alembic. Если вы добавили новые поля в `src/tables.py`, вам нужно:

1. Сгенерировать миграцию внутри контейнера:
   ```bash
   docker compose exec bot alembic revision --autogenerate -m "Описание_изменений"
   ```
2. Применить её к базе:
   ```bash
   docker compose exec bot alembic upgrade head
   ```

---

## 🤖 Доступные команды бота

Добавьте эти команды через `@BotFather` или посмотрите их в чате с ботом по команде `/help`:

- `/list` — Показать активный список задач.
- `/add` — Добавить новую задачу. Поддерживает отмену вводом слова `отмена`.
- `/remove` — Удалить задачу по номеру.
- `/done` — Пометить задачу как выполненную.
- `/remind` — Установить напоминание о задаче.
- `/remlist` — Посмотреть список активных напоминаний.
- `/remremove` — Удалить напоминание, не удаляя задачу.
- `/timezone` — Установить смещение часового пояса (UTC +/- X).
- `/clear` — Очистить весь список.
- `/stats` — Просмотреть статистику и настройки.
- `/help` — Вывести справку по боту.
