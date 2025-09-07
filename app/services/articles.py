from fastapi import Depends
from sqlalchemy.orm import Session

from db.dependencies import get_db


class ArticleService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_articles(self):
        return self.db.query().all()

    def get_article(self, **filters):
        return self.db.query().filter_by(**filters).one_or_none()

    def create_article(self, article_in):
        pass

    def update_article(self, article_in):
        pass

    def delete_article(self, article_in):
        pass


def get_article_service(db: Session = Depends(get_db)) -> ArticleService:
    return ArticleService(db)
