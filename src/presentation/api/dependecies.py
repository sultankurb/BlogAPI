from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from src.infrastructure.redis import get_redis_client

RedisDep = Annotated[Redis, Depends(get_redis_client)]
