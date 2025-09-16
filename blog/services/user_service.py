from models.user_model import User
from repositories.user_repository import UserRepository
from schemas.user_schemas import UserCreate
from validators.user_validator import UserValidator


class UserService:
    def __init__(self, repository: UserRepository, validator: UserValidator) -> None:
        self.repository = repository
        self.validator = validator

    async def create_user(self, user_in: UserCreate) -> User:
        await self.validator.validate_unique_fields(
            username=user_in.username, email=user_in.email
        )

        user_data = user_in.model_dump(mode="json")
        user = await self.repository.create_user(user_data)

        return user
