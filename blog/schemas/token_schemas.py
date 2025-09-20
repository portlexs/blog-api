import uuid
from datetime import datetime

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict

from schemas.user_schemas import PublicUser


class TokenPayload(BaseModel):
    jti: uuid.UUID
    token_type: str
    exp: datetime
    iat: datetime
    user_data: PublicUser

    model_config = SettingsConfigDict(
        json_encoders={datetime: lambda dt: int(dt.timestamp())},
    )


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str
