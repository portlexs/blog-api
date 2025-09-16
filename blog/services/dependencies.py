from typing import Annotated

from fastapi import Depends

from repositories.dependencies import UserRepositoryDep
from services.user_service import UserService
from validators.dependencies import UserValidatorDep


def get_user_service(
    repository: UserRepositoryDep, validator: UserValidatorDep
) -> UserService:
    return UserService(repository, validator)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
