from exceptions.user_exceptions import UserNotFound
from models.user_model import User
from repositories.user_repository import UserRepository
from schemas.user_schemas import UserCreate, UserSearch
from validators.user_validator import UserValidator


class UserService:
    def __init__(self, repository: UserRepository, validator: UserValidator) -> None:
        self.repository = repository
        self.validator = validator

    async def get_user(self, user_in: UserSearch) -> User:
        """
        Returns a user from the database.
        Throws an exception if user not found.
        """
        search_user_data = user_in.model_dump(mode="json", exclude_none=True)
        user = await self.repository.get_user(**search_user_data)
        if user is None:
            raise UserNotFound()
        return user

    async def create_user(self, user_in: UserCreate) -> User:
        """
        Creates and return a new user in the database.
        Throws an exception if the user already exists.
        """
        await self.validator.validate_unique_fields(
            username=user_in.username, email=user_in.email
        )

        user_data = user_in.model_dump(mode="json")
        user = await self.repository.create_user(user_data)

        return user
