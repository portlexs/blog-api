import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.article_model import Article
from ..schemas.article_schemas import ArticleUpdate


class ArticleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_user_articles(self, user_id: str) -> List[Article]:
        query = select(Article).where(Article.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_article(
        self, article_slug: str, user_id: uuid.UUID | None = None
    ) -> Article | None:
        query = select(Article).where(Article.slug == article_slug)
        if user_id:
            query = query.where(Article.user_id == user_id)

        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def create_article(self, article: Article) -> Article:
        self.session.add(article)
        await self.session.commit()
        await self.session.refresh(article)

        return article

    async def update_article(
        self, article: Article, article_in: ArticleUpdate
    ) -> Article:
        article_data = article_in.model_dump(exclude_unset=True)
        for key, value in article_data.items():
            setattr(article, key, value)

        await self.session.commit()
        await self.session.refresh(article)

        return article

    async def delete_article(self, article: Article) -> None:
        await self.session.delete(article)
        await self.session.commit()
