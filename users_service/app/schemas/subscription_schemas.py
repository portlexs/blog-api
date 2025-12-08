import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubscriptionCreate(BaseModel):
    subsсription_key: str


class SubscriptionUpdate(BaseModel):
    author_id: uuid.UUID


class SubscriptionPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    subscriber_id: uuid.UUID
    author_id: uuid.UUID
    created_at: datetime
