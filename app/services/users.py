import uuid

from pydantic import EmailStr
from sqlalchemy.orm import Session

from core.security import hash_password
from models.users import User
from schemas.users import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, user_email: EmailStr) -> User | None:
    return db.query(User).filter(User.email == user_email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    user_data = user_in.model_dump()
    user_data["password"] = hash_password(user_data["password"])

    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, user_id: uuid.UUID, user_in: UserUpdate) -> User:
    db_user = get_user_by_id(db, user_id)
    user_data = user_in.model_dump(exclude_unset=True)

    if "password" in user_data:
        user_data["password"] = hash_password(user_data["password"])

    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user
