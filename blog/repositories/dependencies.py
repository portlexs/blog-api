from typing import Annotated

from fastapi import Depends

from database.dependencies import SessionDep
from repositories.user_repository import UserRepository


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
