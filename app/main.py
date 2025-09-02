import uvicorn
from fastapi import FastAPI

from config import settings
from routes.api_router import api_router


app = FastAPI(title="Blog API")

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.api_host, port=settings.api_port, reload=True)
