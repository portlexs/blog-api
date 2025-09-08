from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from db.dependencies import get_db
from models.articles import Article
from models.users import User
from schemas.articles import (
    ArticleCreate,
    ArticleUpdate,
)


class ArticleService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_articles(self, user: User) -> List[Article]:
        return self.db.query(Article).filter_by(user_id=user.id).all()

    def get_article(self, **filters) -> Article:
        article = self.db.query(Article).filter_by(**filters).one_or_none()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

        return article

    def create_article(self, article_in: ArticleCreate, user: User) -> Article:
        article = Article(**article_in.model_dump(mode="json"), user_id=user.id)

        if self._is_article_exists(slug=article.slug, user=user):
            raise HTTPException(status_code=400, detail="Article title already exists")

        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)

        return article

    def update_article(
        self, slug: str, article_in: ArticleUpdate, user: User
    ) -> Article:
        article = self.get_article(slug=slug, user_id=user.id)

        for key, value in article_in.model_dump(exclude_unset=True).items():
            setattr(article, key, value)

        self.db.commit()
        self.db.refresh(article)

        return article

    def delete_article(self, slug: str, user: User) -> None:
        article = self.get_article(slug=slug, user_id=user.id)

        self.db.delete(article)
        self.db.commit()

    def _is_article_exists(self, slug: str, user: User) -> bool:
        article = (
            self.db.query(Article).filter_by(slug=slug, user_id=user.id).one_or_none()
        )
        return article is not None


def get_article_service(db: Session = Depends(get_db)) -> ArticleService:
    return ArticleService(db)
