from users.user_schemas import UserCreate

from sqlalchemy.ext.asyncio import AsyncSession

from users.user_model import User


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_user(self, user_in: UserCreate) -> User:
        raise NotImplementedError()
