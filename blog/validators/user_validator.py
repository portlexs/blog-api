from exceptions.user_exceptions import UserAlreadyExists
from repositories.user_repository import UserRepository


class UserValidator:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def validate_unique_fields(self, **fields) -> None:
        for field, value in fields.items():
            user = await self.repository.get_user(**{field: value})
            if user:
                raise UserAlreadyExists(field, value)
