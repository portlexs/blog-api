import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    biography: Optional[str] = Field(default=None)
    avatar_url: Optional[HttpUrl] = Field(default=None)


class PublicUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., default_factory=uuid.uuid4)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    biography: Optional[str] = Field(default=None)
    avatar_url: Optional[HttpUrl] = Field(default=None)
    created_at: datetime
    is_active: bool
