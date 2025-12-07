import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException
from jose import jwt, JWTError
from pydantic import ValidationError

from ..schemas.user_schemas import UserCurrent


class JWTService:
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def decode_token(self, token: str) -> UserCurrent:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except (JWTError, ValidationError):
            raise HTTPException(status_code=401, detail="Invalid token")

        user_data = UserCurrent(**payload["user_data"])
        return user_data
