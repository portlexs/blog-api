from typing import Annotated

from fastapi import Depends

from ..database.session import SessionDep
from .token_repository import TokenRepository
from .user_repository import UserRepository


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


def get_token_repository(session: SessionDep) -> TokenRepository:
    return TokenRepository(session)


TokenRepositoryDep = Annotated[TokenRepository, Depends(get_token_repository)]
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
