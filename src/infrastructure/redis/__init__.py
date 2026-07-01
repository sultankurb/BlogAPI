from src.infrastructure.redis import connection


def get_redis_client():
    return connection.redis_client

__all__ = ["get_redis_client"]
