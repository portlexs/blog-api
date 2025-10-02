import uuid
from typing import List

from app.exceptions.comment_exceptions import CommentNotFoundError
from app.models.comment_model import Comment
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment_schemas import CommentCreate
from app.services.article_service import ArticleService


class CommentService:
    def __init__(
        self, comment_repository: CommentRepository, article_service: ArticleService
    ) -> None:
        self.comment_repository = comment_repository
        self.article_service = article_service

    async def get_article_comments(self, article_slug: str) -> List[Comment]:
        article = await self.article_service.get_article(article_slug)
        comments = await self.comment_repository.get_all_comments(article_id=article.id)
        return comments

    async def get_comment(
        self, article_id: uuid.UUID, comment_id: uuid.UUID
    ) -> Comment:
        comment = await self.comment_repository.get_comment(article_id, comment_id)
        if comment is None:
            raise CommentNotFoundError()
        return comment

    async def create_comment(
        self, article_slug: str, comment_in: CommentCreate, user_id: uuid.UUID
    ) -> Comment:
        article = await self.article_service.get_article(article_slug)

        comment_data = comment_in.model_dump(mode="json")
        comment = Comment(**comment_data, user_id=user_id, article_id=article.id)

        comment = await self.comment_repository.create_comment(comment)
        return comment

    async def delete_comment(self, article_slug: str, comment_id: uuid.UUID) -> None:
        article = await self.article_service.get_article(article_slug)
        comment = await self.get_comment(article_id=article.id, comment_id=comment_id)

        await self.comment_repository.delete_comment(comment)
