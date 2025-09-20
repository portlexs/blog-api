from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from config import settings
from repositories.dependencies import UserRepositoryDep
from services.auth_service import AuthService
from services.jwt_service import JWTService
from services.user_service import UserService


@lru_cache
def get_jwt_service() -> JWTService:
    return JWTService(settings.jwt.secret_key, settings.jwt.algorithm)


JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]


def get_auth_service(
    user_repository: UserRepositoryDep, jwt_service: JWTServiceDep
) -> AuthService:
    return AuthService(user_repository, jwt_service)


def get_user_service(user_repository: UserRepositoryDep) -> UserService:
    return UserService(user_repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]


__all__ = ["AuthServiceDep", "JWTServiceDep", "UserServiceDep"]
