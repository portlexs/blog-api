import uuid

from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate


def get_user(db: Session, user_id: uuid.UUID) -> User:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(**user_in)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
