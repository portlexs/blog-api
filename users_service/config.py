from urllib.parse import quote_plus

from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseModel):
    name: str = "test_db"
    host: str = "localhost"
    port: int = 5433
    user: str = "postgres"
    password: str = "password"

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
    secret_key: str = "secret"
    algorithm: str = "HS256"


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    jwt: JWTSettings = JWTSettings()

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
