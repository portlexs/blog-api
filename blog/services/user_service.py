from exceptions.user_exceptions import UserNotFoundError, UserAlreadyExistsError
from models.user_model import User
from repositories.user_repository import UserRepository
from schemas.user_schemas import UserSearch, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_user(self, user_in: UserSearch) -> User:
        user = await self.user_repository.get_user_by_username(user_in.username)
        if user is None:
            raise UserNotFoundError()
        return user

    async def update_user(self, user: User, user_in: UserUpdate) -> User:
        user_data = user_in.model_dump(exclude_unset=True)

        if (
            "username" in user_data
            and await self.user_repository.get_user_by_username(user_data["username"])
            is not None
        ):
            raise UserAlreadyExistsError()

        if (
            "email" in user_data
            and await self.user_repository.get_user_by_email(user_data["email"])
            is not None
        ):
            raise UserAlreadyExistsError()

        return await self.user_repository.update_user(user, user_data)

    async def delete_user(self, user: User) -> None:
        await self.user_repository.update_user(user, {"is_active": False})
