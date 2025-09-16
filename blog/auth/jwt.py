import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Literal, Optional

from jose import jwt, JWTError

from config import settings


TOKEN_EXPIRATION_TIME = {"access": timedelta(minutes=15), "refresh": timedelta(days=7)}


def create_token(token_type: Literal["access", "refresh"], data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + TOKEN_EXPIRATION_TIME[token_type]
    to_encode.update(
        {
            "jti": str(uuid.uuid4()),
            "exp": expire,
            "type": token_type,
            "iat": datetime.now(timezone.utc),
        }
    )

    return jwt.encode(to_encode, settings.jwt.secret_key, settings.jwt.algorithm)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(
            token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm]
        )
        return payload
    except JWTError:
        return None
