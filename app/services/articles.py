from fastapi import Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from db.dependencies import get_db
from schemas.articles import (
    ArticleInfoResponse,
    CreateArticleRequest,
    UpdateArticleRequest,
)


class ArticleService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_articles(self):
        return self.db.query().all()

    def get_article(self, **filters):
        return self.db.query().filter_by(**filters).one_or_none()

    def create_article(self, article_in: CreateArticleRequest) -> ArticleInfoResponse:
        pass

    def update_article(self, article_in: UpdateArticleRequest) -> ArticleInfoResponse:
        pass

    def delete_article(self, slug: str) -> Response:
        pass


def get_article_service(db: Session = Depends(get_db)) -> ArticleService:
    return ArticleService(db)
