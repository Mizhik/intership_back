from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "your_db_user"
    POSTGRES_PASSWORD: str = "your_db_password "
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "your_db_name"

    REDIS_DOMAIN:str = "redis"
    REDIS_PORT:int =6379

    PORT: int = 8000
    HOST: str = "0.0.0.0"
    RELOAD: bool = True
    ALLOWED_ORIGINS: str = "*"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def ASYNC_REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_DOMAIN}:{self.REDIS_PORT}/0"

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


config = Settings()
