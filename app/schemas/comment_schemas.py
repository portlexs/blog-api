import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    body: str = Field(..., min_length=1)


class PublicComment(CommentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    article_id: uuid.UUID
    created_at: datetime


class GetCommentsResponse(BaseModel):
    comments: List[PublicComment]


class CommentUpdate(BaseModel):
    body: str = Field(..., min_length=1)
