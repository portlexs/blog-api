import uvicorn

from fastapi import FastAPI

from .config import settings
from .routers.dependencies import api_router


app = FastAPI(title="Users API", docs_url="/api/users/docs", openapi_url="/api/users/openapi.json")
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app=app, host=settings.api.host, port=settings.api.port)
