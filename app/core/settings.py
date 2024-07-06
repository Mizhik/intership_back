from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "your_db_user"
    DB_PASSWORD: str = "your_db_password "
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "your_db_name"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    RELOAD: bool = True
    ALLOWED_ORIGINS: str = "*"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


config = Settings()
