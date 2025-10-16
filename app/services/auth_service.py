from typing import Tuple

from fastapi.security import HTTPAuthorizationCredentials

from ..core.security import verify_password
from ..exceptions.credentials_exceptions import CredentialsException
from ..exceptions.token_exceptions import InvalidTokenError
from ..exceptions.user_exceptions import (
    InvalidLoginOrPasswordError,
    UserAlreadyExistsError,
    UserNotActiveError,
)
from ..models.user_model import User
from ..repositories.user_repository import UserRepository
from ..schemas.user_schemas import UserCreate, UserDataForToken, UserLogin
from ..services.jwt_service import JWTService


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        jwt_service: JWTService,
    ) -> None:
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def register_user(self, user_in: UserCreate) -> Tuple[str, str]:
        existing_user = await self.user_repository.get_user_by_email_or_username(
            user_in.email, user_in.username
        )
        if existing_user:
            raise UserAlreadyExistsError()

        user = User(**user_in.model_dump(mode="json"))
        new_user = await self.user_repository.create_user(user)
        validated_user_data = UserDataForToken.model_validate(new_user)

        tokens = await self._create_tokens_pair(validated_user_data)
        return tokens

    async def login_user(self, user_in: UserLogin) -> Tuple[str, str]:
        user = await self.user_repository.get_user_by_email_or_username(
            email=user_in.login, username=user_in.login
        )
        if not user or not verify_password(user_in.password, user.password):
            raise InvalidLoginOrPasswordError()

        if not user.is_active:
            raise UserNotActiveError()

        user_data = UserDataForToken.model_validate(user)

        tokens = await self._create_tokens_pair(user_data)
        return tokens

    async def get_current_user(
        self, credentials: HTTPAuthorizationCredentials | None
    ) -> User:
        if not credentials:
            raise CredentialsException("Credentials not found")

        payload = self.jwt_service.decode_token(credentials.credentials)
        if not payload or payload.token_type != "access":
            raise CredentialsException("Invalid token")

        user = await self.user_repository.get_user_by_id(payload.user_data.id)
        if not user:
            raise CredentialsException("User not found")
        elif not user.is_active:
            raise CredentialsException("User is not active")

        return user

    async def refresh_tokens(self, refresh_token: str | None) -> Tuple[str, str]:
        token_payload = self.jwt_service.decode_token(refresh_token)
        if not token_payload or token_payload.token_type != "refresh":
            raise InvalidTokenError("Invalid token")

        token_from_db = await self.jwt_service.get_token(token_payload.jti)
        if not token_from_db or token_from_db.is_revoked:
            raise InvalidTokenError("Invalid token")

        user = await self.user_repository.get_user_by_id(token_payload.user_data.id)
        if not user or not user.is_active:
            raise CredentialsException("Invalid user")

        await self.jwt_service.revoke_token(token_from_db)

        user_data = UserDataForToken.model_validate(token_payload.user_data)
        new_tokens = await self._create_tokens_pair(user_data)

        return new_tokens

    async def _create_tokens_pair(self, user_data: UserDataForToken) -> Tuple[str, str]:
        access_token = self.jwt_service.create_access_token(user_data)
        refresh_token = await self.jwt_service.create_refresh_token(user_data)
        return access_token, refresh_token
