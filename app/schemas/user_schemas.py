import uuid
from datetime import datetime, timezone
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., min_length=3, max_length=50)
    biography: Optional[str] = Field(default=None)
    avatar_url: Optional[HttpUrl] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)


class UserCurrent(UserPublic):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., default_factory=uuid.uuid4)
    email: EmailStr


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    login: Union[str, EmailStr] = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class UserSearch(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(default=None)
    password: Optional[str] = Field(default=None, min_length=8)
    biography: Optional[str] = Field(default=None)
    avatar_url: Optional[HttpUrl] = Field(default=None)


class UserDataForToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
