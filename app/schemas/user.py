from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
    """User read schema"""

    id: int
    email: EmailStr


class UserCreate(BaseModel):
    """User create schema"""

    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """User login schema"""

    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """User update schema"""

    email: Optional[EmailStr] = None
    password: Optional[str] = None
