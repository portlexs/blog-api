import uuid
from typing import Any, Dict, Optional

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_model import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, user_data: Dict[str, Any]) -> User:
        db_user = User(**user_data)

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return db_user

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_user_by_email_or_username(
        self, email: str, username: str
    ) -> Optional[User]:
        query = select(User).where(or_(User.email == email, User.username == username))
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
