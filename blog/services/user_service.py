from exceptions.user_exceptions import UserNotFoundError
from models.user_model import User
from repositories.user_repository import UserRepository
from schemas.user_schemas import UserSearch


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_user(self, user_in: UserSearch) -> User:
        """
        Returns a user from the database.
        Throws an exception if user not found.
        """
        user = await self.user_repository.get_user_by_username(user_in.username)
        if user is None:
            raise UserNotFoundError()
        return user

    # TODO: update user

    # TODO: delete user
