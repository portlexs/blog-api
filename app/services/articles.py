from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from db.dependencies import get_db
from models.articles import Article
from schemas.articles import (
    ArticleCreate,
    ArticleUpdate,
)


class ArticleService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_articles(self) -> List[Article]:
        return self.db.query(Article).all()

    def get_article(self, **filters) -> Article:
        return self.db.query(Article).filter_by(**filters).one_or_none()

    def create_article(self, article_in: ArticleCreate) -> Article:
        article = Article(**article_in.model_dump(mode="json"))

        if self.get_article(slug=article.slug):
            raise HTTPException(status_code=400, detail="article title already exists")

        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)

        return article

    def update_article(self, slug: str, article_in: ArticleUpdate) -> Article:
        article = self.get_article(slug=slug)
        if not article:
            raise HTTPException(status_code=404, detail="article not found")

        for key, value in article_in.model_dump(exclude_unset=True).items():
            setattr(article, key, value)

        self.db.commit()
        self.db.refresh(article)

        return article

    def delete_article(self, slug: str) -> None:
        article = self.get_article(slug=slug)
        if not article:
            raise HTTPException(status_code=404, detail="article not found")

        self.db.delete(article)
        self.db.commit()
        self.db.refresh(article)


def get_article_service(db: Session = Depends(get_db)) -> ArticleService:
    return ArticleService(db)
