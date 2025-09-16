from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth import jwt
from models.user_model import User
from services.dependencies import UserServiceDep


security = HTTPBearer(auto_error=False)


def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
    user_service: UserServiceDep,
) -> User:
    if credentials is None:
        raise credentials_exception()

    payload = jwt.decode_token(credentials.credentials)
    if payload is None or payload.get("id") is None:
        raise credentials_exception()

    if payload.get("type") != "access":
        raise credentials_exception()

    try:
        user = await user_service.get_user(id=payload["id"])
    except HTTPException:
        raise credentials_exception()

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
