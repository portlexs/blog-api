from sqlalchemy.ext.asyncio import AsyncSession

from models.user_model import User
from schemas.user_schemas import UserCreate


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_user(self, user_in: UserCreate) -> User:
        raise NotImplementedError()
