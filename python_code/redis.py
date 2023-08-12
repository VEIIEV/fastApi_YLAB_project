from enum import Enum

import aioredis
from redis.asyncio.client import Redis

from python_code.config import settings


async def get_redis_connection():
    connection: Redis = await aioredis.Redis(port=settings.REDIS_PORT, host=settings.REDIS_HOST,
                                             # encoding='utf8', пока без кодировки
                                             decode_responses=False, db=0)
    return connection


class RedisTable(Enum):
    MENU = 'menu'
    SUBMENU = 'submenu'
    DISH = 'dish'
