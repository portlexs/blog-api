import uvicorn

from app.config import settings


if __name__ == "__main__":
    uvicorn.run(app="app:app", host=settings.api.host, port=settings.api.port)
