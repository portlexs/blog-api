import uuid
from datetime import datetime

from pydantic import BaseModel, field_serializer

from app.schemas.user_schemas import PublicUser


class TokenPayload(BaseModel):
    jti: uuid.UUID
    token_type: str
    exp: datetime
    iat: datetime
    user_data: PublicUser

    @field_serializer("exp")
    def serialize_exp(self, value: datetime) -> int:
        return int(value.timestamp())

    @field_serializer("iat")
    def serialize_iat(self, value: datetime) -> int:
        return int(value.timestamp())


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str
