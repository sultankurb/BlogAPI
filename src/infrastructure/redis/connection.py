import redis.asyncio as aioredis

from src.config import settings

redis_client: aioredis.Redis = None


def init_redis_client():
    global redis_client
    redis_client = aioredis.from_url(
        settings.REDIS_URL,
        max_connections=20,
        socket_timeout=5.0,
        decode_responses=True,
    )
    return redis_client