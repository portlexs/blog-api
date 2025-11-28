ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim AS base

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY alembic.ini .

COPY ./app /app/app

EXPOSE 8000

CMD ["python", "-m", "app.main"]
