# Install Python
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim AS base

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Копируем *только* файлы зависимостей из корня
COPY pyproject.toml poetry.lock ./

# Устанавливаем *все* зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копируем *только* код users_service
COPY ./users_service /app/users_service

# Expose the port that the application listens on.
EXPOSE 8000

# Запускаем конкретно users_service
CMD ["python", "-m", "users_service.main"]
