from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from infrastructure.redis import get_redis_client
from src.infrastructure.database import UnitOfWork, get_uow

UoWDep = Annotated[UnitOfWork, Depends(get_uow)]
RedisDep = Annotated[Redis, Depends(get_redis_client)]
