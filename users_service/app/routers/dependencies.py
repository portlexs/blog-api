from fastapi import APIRouter

from .user_router import router as user_router

api_router = APIRouter(prefix="/api")
api_router.include_router(user_router)
