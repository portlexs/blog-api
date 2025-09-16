from typing import Annotated

from fastapi import Depends

from repositories.dependencies import UserRepositoryDep
from validators.user_validator import UserValidator


def get_user_validator(repository: UserRepositoryDep) -> UserValidator:
    return UserValidator(repository)


UserValidatorDep = Annotated[UserValidator, Depends(get_user_validator)]
