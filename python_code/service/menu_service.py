import pickle
import uuid
from typing import Sequence

from fastapi import HTTPException
from redis.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from python_code.config import settings
from python_code.cruds import menu_crud as MC
from python_code.dao.redis_dao import RedisDAO
from python_code.models.menu_model import Menu
from python_code.schemas.menu_schemas import CreateMenu, MenuSchema
from python_code.utils import add_counters_to_response


async def find_all_menu(r: Redis,
                        request: Request,
                        session: AsyncSession):
    redis: RedisDAO = RedisDAO(r)
    data = redis.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)
    menu: Sequence[Menu] = await MC.get_menu_all(session)
    for elem in menu:
        await add_counters_to_response(elem, session)
    redis.set(key=request.url.path + request.method, value=pickle.dumps(menu),
              expire_time=settings.REDIS_EXPIRE_TIME)
    return menu


async def find_menu_by_id(r: Redis,
                          request: Request,
                          session: AsyncSession,
                          api_test_menu_id: uuid.UUID):
    redis: RedisDAO = RedisDAO(r)
    data = redis.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)
    menu = await MC.get_menu_by_id(api_test_menu_id, session)
    if menu:
        await add_counters_to_response(menu, session)
        redis.set(key=request.url.path + request.method, value=pickle.dumps(menu),
                  expire_time=settings.REDIS_EXPIRE_TIME)
        return menu
    else:
        raise HTTPException(status_code=404, detail='menu not found')


async def create_menu(menu: CreateMenu,
                      r: Redis,
                      request: Request,
                      session: AsyncSession):
    redis: RedisDAO = RedisDAO(r)
    created_menu: MenuSchema | None = await MC.create_menu(menu, session)
    await add_counters_to_response(created_menu, session)
    redis.unvalidate(request.url.path + 'GET')
    return created_menu


async def update_menu_by_id(menu: CreateMenu,
                            api_test_menu_id: uuid.UUID,
                            r: Redis,
                            request: Request,
                            session: AsyncSession):
    redis: RedisDAO = RedisDAO(r)
    menu_id: uuid.UUID | None = await MC.update_menu_by_id(api_test_menu_id, menu, session)
    if menu_id:
        created_menu: MenuSchema | None = await MC.get_menu_by_id(menu_id, session)
        await add_counters_to_response(created_menu, session)
        redis.unvalidate(request.url.path + 'GET',
                         '/api/v1/menusGET')
        return created_menu
    else:
        raise HTTPException(status_code=404, detail='menu not found')


async def delete_menu_by_id(request: Request,
                            api_test_menu_id: uuid.UUID,
                            session: AsyncSession,
                            r: Redis):
    redis: RedisDAO = RedisDAO(r)
    menu_id = await MC.delete_menu_by_id(api_test_menu_id, session)
    if menu_id:
        redis.unvalidate(request.url.path + 'GET',
                         '/api/v1/menusGET')
        return {'status': True,
                'message': 'The menu has been deleted'}
    else:
        raise HTTPException(status_code=404, detail='menu not found')
