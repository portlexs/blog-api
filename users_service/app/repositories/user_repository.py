import uuid
from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user_model import User
from ..schemas.user_schemas import UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_user_by_email_or_username(
        self, email: Optional[str], username: Optional[str]
    ) -> Optional[User]:
        query = select(User).where(or_(User.email == email, User.username == username))
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update_user(self, user: User, user_in: UserUpdate) -> User:
        user_data = user_in.model_dump(mode="json", exclude_unset=True)

        for key, value in user_data.items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def delete_user(self, user: User) -> None:
        setattr(user, "is_active", False)

        await self.session.commit()
        await self.session.refresh(user)
