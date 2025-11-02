from typing import Annotated

from fastapi import Depends

from .article_service import ArticleService
from .comment_service import CommentService
from ..repositories.dependencies import ArticleRepositoryDep, CommentRepositoryDep


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
