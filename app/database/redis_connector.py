from app.core.settings import config
from redis import asyncio as aioredis

# async def get_redis_client():
#     redis = None
#     try:
#         redis = aioredis.ConnectionPool.from_url(config.ASYNC_REDIS_URL)
#         yield aioredis.Redis(connection_pool=redis)
#     finally:
#         if redis:
#             await redis.disconnect()


async def get_redis_client():
    redis = await aioredis.from_url(
        url=config.ASYNC_REDIS_URL, encoding="utf-8", decode_responses=True
    )
    return redis
