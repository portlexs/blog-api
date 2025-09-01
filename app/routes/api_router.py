from fastapi import APIRouter

from routes import articles, comments, users


api_router = APIRouter(prefix="/api")

api_router.include_router(users.router)
api_router.include_router(articles.router)
api_router.include_router(comments.router)
