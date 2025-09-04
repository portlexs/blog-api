import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.jwt import TokenType, create_token
from core.security import verify_password
from db.dependencies import get_db
from services.user import create_user, get_user_by_email, get_user_by_id
from schemas.user import UserCreate, UserLogin, UserLoginResponse, UserRead


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)) -> UserRead:
    """Get user in blog by id"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead.model_validate(user)


@router.post("/")
async def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register user in blog"""
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(db, user_in)
    return UserRead.model_validate(user)


@router.post("/login")
async def login_user(
    user_in: UserLogin, db: Session = Depends(get_db)
) -> UserLoginResponse:
    """Login user in blog"""
    user = get_user_by_email(db, user_in.email)
    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_data = UserRead.model_validate(user)
    token = create_token(TokenType.ACCESS, user_data.model_dump())
    return UserLoginResponse(access_token=token)


@router.put("/{user_id}")
async def update_user(user_id: int) -> dict:
    """Update user in blog by id"""
    return {"message": f"update_user({user_id})"}
