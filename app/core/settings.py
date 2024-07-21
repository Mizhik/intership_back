from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "yourdbuser"
    POSTGRES_PASSWORD: str = "yourdbpassword"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_HOST_SYNC: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "yourdbname"

    REDIS_DOMAIN: str = "redis"
    REDIS_PORT: int = 6379

    PORT: int = 8000
    HOST: str = "0.0.0.0"
    RELOAD: bool = True
    STR_ALLOWED_ORIGINS: str = "*,example.url"

    AUTH_SECRET_KEY: str = "your_secret_key"
    AUTH_ALGORITHM: str = "algorithm"

    DOMAIN: str ="your_domain"
    API_AUDIENCE: str="api_audience"
    ALGORITHM: str="algorithm"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST_SYNC}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def ASYNC_REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_DOMAIN}:{self.REDIS_PORT}/0"

    @property
    def ALLOWED_ORIGINS_LIST(self) -> list:
        return self.STR_ALLOWED_ORIGINS.split(",")

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


config = Settings()
