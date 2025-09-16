# Install Python
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim as base

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock  ./

RUN poetry.lock && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["python", "app/main.py"]
