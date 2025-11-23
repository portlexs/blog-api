import uuid

from pydantic import BaseModel, ConfigDict, Field


class UserCurrent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., default_factory=uuid.uuid4)
