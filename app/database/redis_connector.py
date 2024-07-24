from app.core.settings import config
from redis import asyncio as aioredis

async def get_redis_client():
    redis = None
    try:
        redis = aioredis.ConnectionPool.from_url(config.ASYNC_REDIS_URL)
        yield aioredis.Redis(connection_pool=redis)
    finally:
        if redis:
            await redis.disconnect()
