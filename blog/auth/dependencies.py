from typing import Annotated, Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from exceptions.credentials_exceptions import CredentialsException
from models.user_model import User
from services.dependencies import JWTServiceDep, UserRepositoryDep


security = HTTPBearer(auto_error=False)
SecurityDep = Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)]


async def get_current_user(
    credentials: SecurityDep,
    user_repository: UserRepositoryDep,
    jwt_service: JWTServiceDep,
) -> User:
    if credentials is None:
        raise CredentialsException("Credentials not found")

    payload = jwt_service.decode_token(credentials.credentials)
    if payload is None or payload.token_type != "access":
        raise CredentialsException(f"Invalid token")

    user = await user_repository.get_user_by_id(payload.user_data.id)
    if user is None:
        raise CredentialsException("User not found")
    elif user.is_active is False:
        raise CredentialsException("User is not active")

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
