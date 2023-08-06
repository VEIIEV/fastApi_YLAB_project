from enum import Enum

import redis

from python_code.config import settings


def get_redis_connection():
    return redis.StrictRedis(port=settings.REDIS_PORT, host=settings.REDIS_HOST, encoding='utf8', decode_responses=False, db=0)


class RedisTable(Enum):
    MENU = 'menu'
    SUBMENU = 'submenu'
    DISH = 'dish'
