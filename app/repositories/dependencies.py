from typing import Annotated

from fastapi import Depends

from ..database.session import SessionDep
from .article_repository import ArticleRepository
from .comment_repository import CommentRepository
from .token_repository import TokenRepository
from .user_repository import UserRepository


def get_article_repository(session: SessionDep) -> ArticleRepository:
    return ArticleRepository(session)


def get_comment_repository(session: SessionDep) -> CommentRepository:
    return CommentRepository(session)


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


def get_token_repository(session: SessionDep) -> TokenRepository:
    return TokenRepository(session)


ArticleRepositoryDep = Annotated[ArticleRepository, Depends(get_article_repository)]
CommentRepositoryDep = Annotated[CommentRepository, Depends(get_comment_repository)]
TokenRepositoryDep = Annotated[TokenRepository, Depends(get_token_repository)]
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
