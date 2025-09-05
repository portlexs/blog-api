from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

import services.users as users_service
from core.jwt import decode_token
from db.dependencies import get_db
from models.users import User


security = HTTPBearer()


def get_current_user(
    creaditals: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db),
) -> User:
    creditals_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(creaditals.credentials)
    except JWTError:
        raise creditals_exception

    if payload.get("id") is None:
        raise creditals_exception

    user = users_service.get_user_by_id(db, payload["id"])

    if user is None:
        raise creditals_exception

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
