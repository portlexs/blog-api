import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.comment_model import Comment
from ..schemas.comment_schemas import CommentUpdate


class CommentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_comments(self, article_id: uuid.UUID) -> List[Comment]:
        query = select(Comment).where(Comment.article_id == article_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_comment(
        self, article_id: uuid.UUID, comment_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[Comment]:
        query = select(Comment).where(
            Comment.article_id == article_id,
            Comment.id == comment_id,
            Comment.user_id == user_id,
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def create_comment(self, comment: Comment) -> Comment:
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)

        return comment

    async def update_comment(
        self, comment: Comment, comment_in: CommentUpdate
    ) -> Comment:
        comment_data = comment_in.model_dump(mode="json")

        for key, value in comment_data.items():
            setattr(comment, key, value)

        await self.session.commit()
        await self.session.refresh(comment)

        return comment

    async def delete_comment(self, comment: Comment) -> None:
        await self.session.delete(comment)
        await self.session.commit()
