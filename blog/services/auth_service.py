from typing import Tuple

from auth.security import verify_password
from exceptions.user_exceptions import (
    UserAlreadyExistsError,
    InvalidLoginOrPasswordError,
)
from repositories.user_repository import UserRepository
from schemas.user_schemas import PublicUser, UserCreate, UserLogin
from services.jwt_service import JWTService, TokenType


class AuthService:
    def __init__(
        self, user_repository: UserRepository, jwt_service: JWTService
    ) -> None:
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def register_user(self, user_in: UserCreate) -> Tuple[str, str]:
        existing_user = await self.user_repository.get_user_by_email_or_username(
            user_in.email, user_in.username
        )
        if existing_user is not None:
            raise UserAlreadyExistsError()

        user_data = user_in.model_dump(mode="json")
        user = await self.user_repository.create_user(user_data)
        validated_user_data = PublicUser.model_validate(user)

        tokens = self._create_tokens_pair(validated_user_data)
        return tokens

    async def login_user(self, user_in: UserLogin) -> Tuple[str, str]:
        user = await self.user_repository.get_user_by_email_or_username(
            email=user_in.login, username=user_in.login
        )
        if user is None or not verify_password(user_in.password, user.password):
            raise InvalidLoginOrPasswordError()

        user_data = PublicUser.model_validate(user)

        tokens = self._create_tokens_pair(user_data)
        return tokens

    def _create_tokens_pair(self, user_data: PublicUser) -> Tuple[str, str]:
        access_token = self.jwt_service.create_token(TokenType.ACCESS, user_data)
        refresh_token = self.jwt_service.create_token(TokenType.REFRESH, user_data)
        return access_token, refresh_token
