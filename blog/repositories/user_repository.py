from typing import Any, Dict, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_model import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user(self, **filters) -> Optional[User]:
        query = select(User).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def create_user(self, user_data: Dict[str, Any]) -> User:
        db_user = User(**user_data)

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return db_user
