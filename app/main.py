import uvicorn
from fastapi import FastAPI

# from .config import settings
from .routers import api_router


app = FastAPI(title="Blog API")
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app=app)
