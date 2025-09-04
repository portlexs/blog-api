from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.jwt import TokenType, create_token
from core.security import verify_password
from db.dependencies import get_db
from services.user import create_user, get_user_by_email, get_user_by_id
from schemas.user import UserCreate


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user in blog by id"""
    return get_user_by_id(db, user_id)


@router.post("/")
async def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register user in blog"""
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(db, user_in)
    return user


@router.post("/login")
async def login_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Login user in blog"""
    user = get_user_by_email(db, user_in.email)
    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token(TokenType.ACCESS, {"id": user.id, "email": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.put("/{user_id}")
async def update_user(user_id: int) -> dict:
    """Update user in blog by id"""
    return {"message": f"update_user({user_id})"}
