from typing import Tuple

from fastapi.security import HTTPAuthorizationCredentials

from auth.security import verify_password
from exceptions.credentials_exceptions import CredentialsException
from exceptions.user_exceptions import (
    UserAlreadyExistsError,
    InvalidLoginOrPasswordError,
)
from models.user_model import User
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

        user = User(**user_in.model_dump(mode="json"))
        new_user = await self.user_repository.create_user(user)
        validated_user_data = PublicUser.model_validate(new_user)

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

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials) -> User:
        if credentials is None:
            raise CredentialsException("Credentials not found")

        payload = self.jwt_service.decode_token(credentials.credentials)
        if payload is None or payload.token_type != "access":
            raise CredentialsException(f"Invalid token")

        user = await self.user_repository.get_user_by_id(payload.user_data.id)
        if user is None:
            raise CredentialsException("User not found")
        elif user.is_active is False:
            raise CredentialsException("User is not active")

        return user

    def refresh_tokens(self, current_user: User) -> Tuple[str, str]:
        user_data = PublicUser.model_validate(current_user)

        tokens = self._create_tokens_pair(user_data)
        return tokens

    def _create_tokens_pair(self, user_data: PublicUser) -> Tuple[str, str]:
        access_token = self.jwt_service.create_token(TokenType.ACCESS, user_data)
        refresh_token = self.jwt_service.create_token(TokenType.REFRESH, user_data)
        return access_token, refresh_token
