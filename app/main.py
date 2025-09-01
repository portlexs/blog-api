import uvicorn
from fastapi import FastAPI

from routes.api_router import api_router


app = FastAPI(title="Blog API")

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
