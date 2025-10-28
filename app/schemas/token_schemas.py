import uuid
from datetime import datetime

from pydantic import BaseModel, field_serializer

from ..schemas.user_schemas import UserDataForToken


class TokenPayload(BaseModel):
    jti: uuid.UUID
    token_type: str
    exp: datetime
    iat: datetime
    user_data: UserDataForToken

    @field_serializer("exp")
    def serialize_exp(self, value: datetime) -> int:
        return int(value.timestamp())

    @field_serializer("iat")
    def serialize_iat(self, value: datetime) -> int:
        return int(value.timestamp())


class AuthTokens(BaseModel):
    access_token: str
