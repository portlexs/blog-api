from urllib.parse import quote_plus

from pydantic import BaseModel, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class DBSettings(BaseModel):
    name: str
    host: str
    port: int
    user: str
    password: str

    @computed_field
    def encoded_password(self) -> str:
        return quote_plus(self.password)

    @computed_field
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.encoded_password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class JWTSettings(BaseModel):
    secret_key: str = "secret_key"
    algorithm: str = "HS256"


class CelerySettings(BaseModel):
    broker_url: str = "redis://redis_broker:6380/0"


class Settings(BaseSettings):
    api: APISettings = Field(validation_alias="BLOG_API")
    jwt: JWTSettings = JWTSettings()
    db: DBSettings = Field(validation_alias="BLOG_DB")
    celery: CelerySettings = CelerySettings()

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
