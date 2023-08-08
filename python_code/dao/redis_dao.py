from typing import Any

from redis.client import Redis


class RedisDAO:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get(self, key: str) -> Any | None:
        return self.redis.get(key)

    def set(self, key: str, value: bytes, expire_time: int = 60) -> None:
        self.redis.set(key, value)
        self.redis.expire(key, expire_time)

    def unvalidate(self, *keys: Any):
        self.redis.delete(*keys)
