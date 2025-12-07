from typing import Annotated

from fastapi import Depends, HTTPException, status

from .article_service import ArticleService
from ..config import settings
from ..core.security import SecurityDep
from .comment_service import CommentService
from ..repositories.dependencies import ArticleRepositoryDep, CommentRepositoryDep
from ..schemas.user_schemas import UserCurrent
from ..services.jwt_service import JWTService


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


def get_jwt_service() -> JWTService:
    return JWTService(
        secret_key=settings.jwt.secret_key, algorithm=settings.jwt.algorithm
    )


JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]


async def get_current_user(
    jwt_service: JWTServiceDep, credentials: SecurityDep
) -> UserCurrent:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return jwt_service.decode_token(credentials.credentials)


CurrentUserDep = Annotated[UserCurrent, Depends(get_current_user)]
