from typing import Annotated

from fastapi import Depends

from .auth_service import AuthService
from ..config import settings
from ..core.security import SecurityDep
from .jwt_service import JWTService
from ..models.user_model import User
from ..repositories.dependencies import (
    TokenRepositoryDep,
    UserRepositoryDep,
)
from .user_service import UserService


def get_jwt_service(token_repository: TokenRepositoryDep) -> JWTService:
    return JWTService(settings.jwt.secret_key, settings.jwt.algorithm, token_repository)


JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]


def get_auth_service(
    user_repository: UserRepositoryDep, jwt_service: JWTServiceDep
) -> AuthService:
    return AuthService(user_repository, jwt_service)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_user_service(user_repository: UserRepositoryDep) -> UserService:
    return UserService(user_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
    auth_service: AuthServiceDep, credentials: SecurityDep
) -> User:
    return await auth_service.get_current_user(credentials)


CurrentUserDep = Annotated[User, Depends(get_current_user)]
