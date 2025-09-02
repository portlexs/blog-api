from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_host: str
    api_port: int

    jwt_secret_key: str
    jwt_algorithm: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
