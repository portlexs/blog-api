import uvicorn

from fastapi import FastAPI

from .config import get_settings
from .routers.dependencies import api_router
from .utils.app_lifespan import lifespan


app = FastAPI(title="Blog API", lifespan=lifespan)
app.include_router(api_router)


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(app=app, host=settings.api.host, port=settings.api.port)
