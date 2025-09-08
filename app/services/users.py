from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import core.jwt as jwt
from core.security import verify_password
from db.dependencies import get_db
from models.users import User
from schemas.users import (
    UserCreateRequest,
    UserInfoResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdateRequest,
)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, **filters) -> User | None:
        return self.db.query(User).filter_by(**filters).one_or_none()

    def register_user(self, user_in: UserCreateRequest) -> UserInfoResponse:
        if self.get_user(email=user_in.email) or self.get_user(
            username=user_in.username
        ):
            raise HTTPException(status_code=400, detail="User already exists")

        user_data = user_in.model_dump(mode="json")
        user = User(**user_data)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return UserInfoResponse.model_validate(user)

    def login_user(self, user_in: UserLoginRequest) -> UserLoginResponse:
        user = self.get_user(email=user_in.email)
        if not (user and verify_password(user_in.password, user.password)):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return self._generate_tokens(user)

    def update_user(self, user: User, user_in: UserUpdateRequest) -> UserInfoResponse:
        user_data = user_in.model_dump(exclude_unset=True)

        if "username" in user_data and self.get_user(username=user_data["username"]):
            raise HTTPException(status_code=400, detail="Username already exists")

        if "email" in user_data and self.get_user(email=user_data["email"]):
            raise HTTPException(status_code=400, detail="Email already exists")

        for key, value in user_data.items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)

        return UserInfoResponse.model_validate(user)

    def refresh_user_token(self, refresh_token: str) -> UserLoginResponse:
        payload = jwt.decode_token(refresh_token)

        if not payload or payload.get("type") != "refresh" or payload.get("id") is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        current_user = self.get_user(id=payload["id"])
        if not current_user:
            raise HTTPException(status_code=401, detail="User not found")

        return self._generate_tokens(current_user)

    def _generate_tokens(self, user: User) -> UserLoginResponse:
        user_data = UserInfoResponse.model_validate(user)

        access_token = jwt.create_token("access", user_data.model_dump(mode="json"))
        refresh_token = jwt.create_token("refresh", {"id": str(user_data.id)})

        return UserLoginResponse(access_token=access_token, refresh_token=refresh_token)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
