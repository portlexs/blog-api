import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from auth.security import hash_password
from db.session import Base
from models.articles import Article


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password: Mapped[str] = mapped_column(String(128))
    username: Mapped[str] = mapped_column(String(50), unique=True)
    bio: Mapped[str] = mapped_column(String(255), nullable=True)
    image_url: Mapped[str] = mapped_column(String(2048), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_banned: Mapped[bool] = mapped_column(default=False)

    articles: Mapped[list["Article"]] = relationship(cascade="all, delete-orphan")

    @validates("password")
    def validate_password(self, key, password: str) -> str:
        return hash_password(password)
