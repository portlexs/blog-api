import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data["id"] = str(data["id"])
        return data


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
