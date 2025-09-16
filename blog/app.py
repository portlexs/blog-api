from typing import Dict

from fastapi import APIRouter, FastAPI, status

from users.user_router import router as users_router


api_router = APIRouter(prefix="/api")
api_router.include_router(users_router)


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
