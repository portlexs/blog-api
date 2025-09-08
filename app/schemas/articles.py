import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3)
    body: str = Field(..., min_length=3)
    tag_list: Optional[List[str]] = Field(default_factory=list)


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, min_length=3)
    body: Optional[str] = Field(None, min_length=3)
    tag_list: Optional[List[str]] = Field(default_factory=list)


class ArticleInfoResponse(ArticleCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str = Field(..., min_length=3, max_length=50)
    created_at: datetime


class AllArticlesResponse(BaseModel):
    articles: List[ArticleInfoResponse]
