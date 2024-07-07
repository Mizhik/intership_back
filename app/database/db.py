import contextlib

from redis import asyncio as aioredis

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import config


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as error:
            print(error)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.ASYNC_DATABASE_URL)


async def get_db():
    async with sessionmanager.session() as session:
        yield session


async def get_redis_client():
    redis = None
    try:
        redis = aioredis.ConnectionPool.from_url(config.ASYNC_REDIS_URL)
        yield aioredis.Redis(connection_pool=redis)
    finally:
        if redis:
            await redis.disconnect()
