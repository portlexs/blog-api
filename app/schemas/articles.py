import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


class BaseArticle(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str
    body: str
    tag_list: Optional[List[str]]


class ArticleInfoResponse(BaseArticle):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str = Field(..., min_length=3, max_length=50)
    created_at: datetime
    is_deleted: bool


class AllArticlesResponse(BaseModel):
    articles: List[ArticleInfoResponse]
    articles_count: int


class CreateArticleRequest(BaseArticle):
    pass


class UpdateArticleRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str]
    body: Optional[str]
    tag_list: Optional[List[str]]
