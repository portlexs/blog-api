from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict

from jose import jwt

from config import settings


class TokenType(Enum):
    ACCESS = timedelta(minutes=15)
    REFRESH = timedelta(days=7)


def create_token(token_type: TokenType, data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + token_type.value
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.jwt.secret_key, settings.jwt.algorithm)


def decode_token(token: str) -> Dict[str, Any]:
    payload = jwt.decode(
        token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm]
    )
    return payload
