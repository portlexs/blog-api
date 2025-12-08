from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    name: str
    host: str
    port: int
    user: str
    password: str

    @computed_field
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    db: DBSettings = Field(validation_alias="USERS_DB")
    celery_broker_url: str = "redis://redis_broker:6379/0"
    push_service_url: str = "http://push_notificator:8000/api/v1/notify"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
