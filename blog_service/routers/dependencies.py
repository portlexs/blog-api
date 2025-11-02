from typing import Dict

from fastapi import APIRouter, status

from .article_router import router as article_router
from .comments_router import router as comments_router


api_router = APIRouter(prefix="/api")

api_router.include_router(article_router)
api_router.include_router(comments_router)


@api_router.get(
    path="/health",
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    tags=["health"],
)
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}
