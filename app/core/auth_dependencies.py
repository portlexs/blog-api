from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

import services.users as users_service
from core.jwt import decode_token
from db.dependencies import get_db
from models.users import User


security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Session = Depends(get_db),
) -> User:
    def creditals_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials is None:
        raise creditals_exception()

    payload = decode_token(credentials.credentials)
    if payload is None or payload.get("id") is None:
        raise creditals_exception()

    user = users_service.get_user_by_id(db, payload["id"])
    if user is None:
        raise creditals_exception()

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
