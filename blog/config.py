from pathlib import Path
from urllib.parse import quote_plus

from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


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
            f"postgresql+psycopg2://{self.user}:{self.encoded_password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class JWTSettings(BaseModel):
    secret_key: str
    algorithm: str = "HS256"


class Settings(BaseSettings):
    api: APISettings
    db: DBSettings
    jwt: JWTSettings
    test_db: DBSettings

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
