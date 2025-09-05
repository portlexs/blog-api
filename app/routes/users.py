from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import services.users as users_service
from core.auth_dependencies import CurrentUser
from core.jwt import TokenType, create_token
from core.security import verify_password
from db.dependencies import get_db
from schemas.users import UserCreate, UserLogin, UserLoginResponse, UserRead, UserUpdate


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_current_user(current_user: CurrentUser) -> UserRead:
    """Get current user in blog"""
    return UserRead.model_validate(current_user)


@router.post("/")
async def register_user(user_in: UserCreate, db: Session = Depends(get_db)) -> UserRead:
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


@router.put("/me")
async def update_user(
    user_in: UserUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> UserRead:
    """Update user in blog by id"""
    if user_in.email and users_service.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    updated_user = users_service.update_user(db, current_user.id, user_in)
    return UserRead.model_validate(updated_user)
