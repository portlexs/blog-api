import uuid
from datetime import datetime, timezone
from typing import Optional

from jose import jwt, JWTError
from pydantic import ValidationError

from ..enums.token_type import TokenType
from ..models.token_model import Token
from ..repositories.token_repository import TokenRepository
from ..schemas.token_schemas import TokenPayload
from ..schemas.user_schemas import UserDataForToken


class JWTService:
    def __init__(
        self, secret_key: str, algorithm: str, token_repository: TokenRepository
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_repository = token_repository

    async def get_token(self, jti: uuid.UUID) -> Optional[Token]:
        return await self.token_repository.get_token(jti)

    def create_access_token(self, user_data: UserDataForToken) -> str:
        token_payload = self._create_token_payload(TokenType.ACCESS, user_data)

        access_token = self._encode_token(token_payload)
        return access_token

    async def create_refresh_token(self, user_data: UserDataForToken) -> str:
        token_payload = self._create_token_payload(TokenType.REFRESH, user_data)

        await self.token_repository.save_token(token_payload)

        token = self._encode_token(token_payload)
        return token

    def decode_token(self, token: str | None) -> Optional[TokenPayload]:
        if not token:
            return None
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenPayload(**payload)
        except (JWTError, ValidationError):
            return None

    async def revoke_token(self, token: Token) -> Token:
        return await self.token_repository.revoke_token(token)

    def _create_token_payload(
        self, token_type: TokenType, user_data: UserDataForToken
    ) -> TokenPayload:
        datetime_now = datetime.now(timezone.utc)
        exp = datetime_now + token_type.value

        token_payload = TokenPayload(
            jti=uuid.uuid4(),
            token_type=token_type.name.lower(),
            exp=exp,
            iat=datetime_now,
            user_data=user_data,
        )

        return token_payload

    def _encode_token(self, token_payload: TokenPayload) -> str:
        return jwt.encode(
            token_payload.model_dump(mode="json"), self.secret_key, self.algorithm
        )
