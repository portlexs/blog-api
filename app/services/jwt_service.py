import uuid
from datetime import datetime, timezone
from typing import Optional

from jose import jwt, JWTError
from pydantic import ValidationError

from app.enums.token_type import TokenType
from app.schemas.token_schemas import TokenPayload
from app.schemas.user_schemas import UserDataForToken


class JWTService:
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, token_type: TokenType, user_data: UserDataForToken) -> str:
        datetime_now = datetime.now(timezone.utc)
        exp = datetime_now + token_type.value

        token_payload = TokenPayload(
            jti=uuid.uuid4(),
            token_type=token_type.name.lower(),
            exp=exp,
            iat=datetime_now,
            user_data=user_data,
        )

        token = jwt.encode(
            token_payload.model_dump(mode="json"),
            self.secret_key,
            self.algorithm,
        )

        return token

    def decode_token(self, token: str) -> Optional[TokenPayload]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenPayload(**payload)
        except (JWTError, ValidationError):
            return None
