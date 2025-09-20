from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from auth.security import SecurityDep
from config import settings
from models.user_model import User
from repositories.dependencies import (
    ArticleRepositoryDep,
    CommentRepositoryDep,
    UserRepositoryDep,
)
from services.article_service import ArticleService
from services.auth_service import AuthService
from services.comment_service import CommentService
from services.jwt_service import JWTService
from services.user_service import UserService


@lru_cache
def get_jwt_service() -> JWTService:
    return JWTService(settings.jwt.secret_key, settings.jwt.algorithm)


JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]


def get_auth_service(
    user_repository: UserRepositoryDep, jwt_service: JWTServiceDep
) -> AuthService:
    return AuthService(user_repository, jwt_service)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_user_service(user_repository: UserRepositoryDep) -> UserService:
    return UserService(user_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
    auth_service: AuthServiceDep, credentials: SecurityDep
) -> User:
    return await auth_service.get_current_user(credentials)


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_article_service(
    article_repository: ArticleRepositoryDep,
) -> ArticleService:
    return ArticleService(article_repository)


ArticleServiceDep = Annotated[ArticleService, Depends(get_article_service)]


def get_comment_service(
    comment_repository: CommentRepositoryDep, article_service: ArticleServiceDep
) -> CommentService:
    return CommentService(comment_repository, article_service)


CommentServiceDep = Annotated[CommentService, Depends(get_comment_service)]
