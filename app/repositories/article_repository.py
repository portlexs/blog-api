import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article_model import Article
from app.schemas.article_schemas import ArticleUpdate


class ArticleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_articles(self, user_id: uuid.UUID) -> List[Article]:
        query = select(Article).where(Article.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_article(
        self, article_slug: str, user_id: Optional[uuid.UUID]
    ) -> Optional[Article]:
        if user_id:
            article = select(Article).where(
                Article.slug == article_slug, Article.user_id == user_id
            )
        else:
            article = select(Article).where(Article.slug == article_slug)

        result = await self.session.execute(article)
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
