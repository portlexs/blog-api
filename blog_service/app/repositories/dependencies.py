from typing import Annotated

from fastapi import Depends

from ..database.session import SessionDep
from .article_repository import ArticleRepository
from .comment_repository import CommentRepository


def get_article_repository(session: SessionDep) -> ArticleRepository:
    return ArticleRepository(session)


def get_comment_repository(session: SessionDep) -> CommentRepository:
    return CommentRepository(session)


ArticleRepositoryDep = Annotated[ArticleRepository, Depends(get_article_repository)]
CommentRepositoryDep = Annotated[CommentRepository, Depends(get_comment_repository)]
