from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.dependencies import get_db
from models.user import User
from services.user import get_user, create_user
from schemas.user import UserCreate


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: int) -> dict:
    """Get user in blog by id"""
    return {"message": f"get_user({user_id})"}


@router.post("/")
async def register_user(user_in: UserCreate, db: Session = Depends(get_db)) -> User:
    """Register user in blog"""
    if get_user(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(db, user_in)
    return user


@router.post("/login")
async def login_user() -> dict:
    """Login user in blog"""
    return {"message": "login_user()"}


@router.put("/{user_id}")
async def update_user(user_id: int) -> dict:
    """Update user in blog by id"""
    return {"message": f"update_user({user_id})"}
