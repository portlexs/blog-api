import uuid
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from db.dependencies import get_db
from models.comments import Comment
from models.users import User
from schemas.comments import CommentCreate
from services.articles import ArticleService, get_article_service


class CommentService:
    def __init__(self, db: Session):
        self.db = db

    def get_artile_comments(
        self,
        article_slug: str,
        article_service: ArticleService = Depends(get_article_service),
    ) -> List[Comment]:
        article = article_service.get_article(slug=article_slug)
        return article.comments

    def get_comment(self, **filters) -> Comment:
        comment = self.db.query(Comment).filter_by(**filters).one_or_none()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        return comment

    def create_comment(
        self,
        article_slug: str,
        comment_in: CommentCreate,
        user: User,
        article_service: ArticleService = Depends(get_article_service),
    ) -> Comment:
        article = article_service.get_article(slug=article_slug)
        comment = Comment(
            **comment_in.model_dump(mode="json"), user_id=user.id, article_id=article.id
        )

        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)

        return comment

    def delete_comment(
        self,
        article_slug: str,
        comment_id: uuid.UUID,
        article_service: ArticleService = Depends(get_article_service),
    ) -> None:
        article = article_service.get_article(slug=article_slug)
        comment = self.get_comment(article_id=article.id, id=comment_id)

        self.db.delete(comment)
        self.db.commit()


def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(db)
