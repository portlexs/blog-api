import uuid

from pydantic import EmailStr
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, user_email: EmailStr) -> User:
    return db.query(User).filter(User.email == user_email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(**user_in)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
