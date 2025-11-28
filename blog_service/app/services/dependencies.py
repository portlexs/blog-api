from typing import Annotated

import httpx
from fastapi import Depends, HTTPException, status

from .article_service import ArticleService
from ..core.security import SecurityDep
from .comment_service import CommentService
from ..repositories.dependencies import ArticleRepositoryDep, CommentRepositoryDep
from ..schemas.user_schemas import UserCurrent


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


async def get_current_user(credentials: SecurityDep) -> UserCurrent:
    url = "http://users_service:8000/api/users/me"
    headers = {"Authorization": f"Bearer {credentials.credentials}"}

    async with httpx.AsyncClient() as client:
        try:
            user_response = await client.get(url, headers=headers)
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Users service is unavailable",
            )

    if user_response.status_code != 200:
        raise HTTPException(
            status_code=user_response.status_code,
            detail=f"User service error: {user_response.json()['detail']}",
        )
    user_data = user_response.json()
    return UserCurrent(**user_data)


CurrentUserDep = Annotated[UserCurrent, Depends(get_current_user)]
