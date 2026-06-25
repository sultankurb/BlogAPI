import redis.asyncio as aioredis

from src.config import settings

redis_client = aioredis.from_url(
    url=settings.REDIS_URL,
)
