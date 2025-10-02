from app.exceptions.user_exceptions import UserNotFoundError, UserAlreadyExistsError
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserSearch, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_user(self, user_in: UserSearch) -> User:
        user = await self.user_repository.get_user_by_username(user_in.username)
        if user is None:
            raise UserNotFoundError()
        return user

    async def update_user(self, user: User, user_in: UserUpdate) -> User:
        if (
            user_in.username is not None
            and await self.user_repository.get_user_by_username(user_in.username)
            is not None
        ):
            raise UserAlreadyExistsError()

        if (
            user_in.email is not None
            and await self.user_repository.get_user_by_email(user_in.email) is not None
        ):
            raise UserAlreadyExistsError()

        return await self.user_repository.update_user(user, user_in)

    async def delete_user(self, user: User) -> None:
        await self.user_repository.update_user(user, {"is_active": False})
