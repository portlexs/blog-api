import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    body: str


class CommentDelete(BaseModel):
    id: uuid.UUID
    article_id: uuid.UUID


class CommentInfoResponse(CommentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    article_id: uuid.UUID
    created_at: datetime


class GetCommentsResponse(BaseModel):
    comments: List[CommentInfoResponse]
