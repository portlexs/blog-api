import uuid
from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel, ConfigDict, EmailStr, Field


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserCreate(UserLogin):
    username: str = Field(..., min_length=3, max_length=50)
    bio: Optional[str] = Field(None, max_length=255)
    image_url: Optional[AnyUrl] = Field(None, max_length=2048)


class UserInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    bio: Optional[str] = Field(None, max_length=255)
    image_url: Optional[AnyUrl] = None
    created_at: datetime
    is_banned: bool


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6)
    bio: Optional[str] = Field(None, max_length=255)
    image_url: Optional[str] = Field(None, max_length=2048)


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
