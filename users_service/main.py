import uvicorn

from fastapi import FastAPI

from .config import settings
from .routers.user_router import router


app = FastAPI(title="Blog API")
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app=app, host=settings.api.host, port=settings.api.port)
