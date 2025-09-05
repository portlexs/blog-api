import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data["id"] = str(data["id"])
        return data


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
