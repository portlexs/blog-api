from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """User base schema"""

    email: EmailStr


class UserRead(UserBase):
    """User read schema"""

    id: int


class UserCreate(UserBase):
    """User create schema"""

    password: str


class UserUpdate(BaseModel):
    """User update schema"""

    email: Optional[EmailStr] = None
    password: Optional[str] = None
