from urllib.parse import quote_plus

from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseModel):
    host: str
    port: int


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


class Settings(BaseSettings):
    api: APISettings
    db: DBSettings

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
