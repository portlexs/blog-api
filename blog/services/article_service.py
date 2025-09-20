import uuid
from typing import List, Optional

from exceptions.article_exceptions import ArticleNotFoundError
from models.article_model import Article
from repositories.article_repository import ArticleRepository
from schemas.article_schemas import ArticleCreate, ArticleUpdate


class ArticleService:
    def __init__(self, article_repository: ArticleRepository) -> None:
        self.article_repository = article_repository

    async def get_all_articles(self, user_id: uuid.UUID) -> List[Article]:
        return await self.article_repository.get_all_articles(user_id=user_id)

    async def get_article(
        self, article_slug: str, user_id: Optional[uuid.UUID] = None
    ) -> Article:
        article = await self.article_repository.get_article(article_slug, user_id)
        if article is None:
            raise ArticleNotFoundError()
        return article

    async def create_article(
        self, article_in: ArticleCreate, user_id: uuid.UUID
    ) -> Article:
        article_data = article_in.model_dump(exclude_unset=True)

        article = Article(**article_data, user_id=user_id)
        new_article = await self.article_repository.create_article(article)

        return new_article

    async def update_article(
        self, article_slug: str, article_in: ArticleUpdate, user_id: uuid.UUID
    ) -> Article:
        article = await self.get_article(article_slug, user_id)

        updated_article = await self.article_repository.update_article(
            article, article_in
        )
        return updated_article

    async def delete_article(self, article_slug: str, user_id: uuid.UUID) -> None:
        article = await self.get_article(article_slug, user_id)
        await self.article_repository.delete_article(article)
