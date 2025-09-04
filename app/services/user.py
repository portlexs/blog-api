import uuid

from pydantic import EmailStr
from sqlalchemy.orm import Session

from core.security import hash_password
from models.user import User
from schemas.user import UserCreate


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, user_email: EmailStr) -> User:
    return db.query(User).filter(User.email == user_email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    user_data = user_in.model_dump()
    user_data["password"] = hash_password(user_data["password"])

    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
