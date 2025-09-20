from typing import Annotated

from fastapi import Depends

from database.dependencies import SessionDep
from repositories.article_repository import ArticleRepository
from repositories.comment_repository import CommentRepository
from repositories.user_repository import UserRepository


def get_article_repository(session: SessionDep) -> ArticleRepository:
    return ArticleRepository(session)


def get_comment_repository(session: SessionDep) -> CommentRepository:
    return CommentRepository(session)


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


ArticleRepositoryDep = Annotated[ArticleRepository, Depends(get_article_repository)]
CommentRepositoryDep = Annotated[CommentRepository, Depends(get_comment_repository)]
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
