from typing import Dict

from fastapi import APIRouter, status

from routes import articles, comments, users


api_router = APIRouter(prefix="/api")


@api_router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> Dict[str, str]:
    return {"status": "ok"}


api_router.include_router(users.router)
api_router.include_router(articles.router)
api_router.include_router(comments.router)
