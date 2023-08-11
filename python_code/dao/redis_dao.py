from typing import Any

from redis.asyncio.client import Redis


class RedisDAO:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> Any | None:
        return await self.redis.get(key)

    async def set(self, key: str, value: bytes, expire_time: int = 60) -> None:
        await self.redis.set(key, value)
        await self.redis.expire(key, expire_time)

    async def unvalidate(self, *keys: Any):
        await self.redis.delete(*keys)
