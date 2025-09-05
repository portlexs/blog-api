import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import services.users as users_service
from core.jwt import TokenType, create_token
from core.security import verify_password
from db.dependencies import get_db
from schemas.users import UserCreate, UserLogin, UserLoginResponse, UserRead, UserUpdate


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)) -> UserRead:
    """Get user in blog by id"""
    user = users_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead.model_validate(user)


@router.post("/")
async def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register user in blog"""
    if users_service.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = users_service.create_user(db, user_in)
    return UserRead.model_validate(user)


@router.post("/login")
async def login_user(
    user_in: UserLogin, db: Session = Depends(get_db)
) -> UserLoginResponse:
    """Login user in blog"""
    user = users_service.get_user_by_email(db, user_in.email)
    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_data = UserRead.model_validate(user)
    token = create_token(TokenType.ACCESS, user_data.model_dump())
    return UserLoginResponse(access_token=token)


@router.put("/{user_id}")
async def update_user(
    user_id: uuid.UUID, user_in: UserUpdate, db: Session = Depends(get_db)
) -> UserRead:
    """Update user in blog by id"""
    db_user = users_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_in.email:
        if users_service.get_user_by_email(db, user_in.email):
            raise HTTPException(status_code=400, detail="Email already registered")

    updated_user = users_service.update_user(db, user_id, user_in)
    return UserRead.model_validate(updated_user)
