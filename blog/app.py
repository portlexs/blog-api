from typing import Dict

from fastapi import APIRouter, FastAPI, status

from routers.article_router import router as article_router
from routers.user_router import router as user_router


api_router = APIRouter(prefix="/api")
api_router.include_router(article_router)
api_router.include_router(user_router)


@api_router.get(
    path="/health",
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    tags=["health"],
)
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}


app = FastAPI(title="Blog API")
app.include_router(api_router)
