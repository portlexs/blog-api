ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim

# Установка необходимых системных зависимостей
# libpq-dev нужен для psycopg2/asyncpg, если не используются бинарные колеса,
# curl - для healthcheck (если нужен)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock* ./

# Настройка poetry: не создавать виртуальное окружение (ставим в системный python контейнера)
# и установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копирование исходного кода приложения
COPY ./app /app/app

# Пользователь не root (хорошая практика, но для лабы необязательно)
# USER nobody

# Команда запуска по умолчанию
# Запускаем Celery воркер, указывая путь к приложению (app.main)
CMD ["celery", "-A", "app.main", "worker", "--loglevel=info"]
