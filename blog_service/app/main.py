import uvicorn

from fastapi import FastAPI

from .config import settings
from .routers.dependencies import api_router


app = FastAPI(title="Blog API", docs_url=None, redoc_url=None,openapi_url="/api/openapi.json")
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app=app, host=settings.api.host, port=settings.api.port)
