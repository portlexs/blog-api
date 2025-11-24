# RESTful Blog API

## Описание

Это приложение содержит асинхронноое RESTful API на языке Python с применением библиотек FastAPI, SQLAlchemy, Alembic. С помощью API блога можно совершать различные операции над пользователями, статьями и комментариями. Все операции храняться в базе данных PostgreSQL.

## Требования для запуска

- Установленный Docker

## Запуск приложения

1. Клонируйте репозиторий:

```bash
git clone https://github.com/portlexs/microservice-architecture
```

2. Скопируйте переменные окружения в файл `.env` из файла `.env.example` и измените их при необходимости.

3. Запустите сборку Docker образа:

```bash
docker compose -p blog_api up --build
```

4. Переходите по ссылкам
   - http://localhost/api/users/docs,
   - http://localhost/api/docs
