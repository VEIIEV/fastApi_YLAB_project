import pickle
import uuid

from fastapi import HTTPException
from redis.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from python_code.config import settings
from python_code.cruds import menu_crud as MC
from python_code.cruds import submenu_crud as SC
from python_code.dao.redis_dao import RedisDAO
from python_code.schemas.submenu_schemas import (
    BaseSubmenu,
    CreateSubmenu,
    SubmenuSchema,
)
from python_code.utils import add_dish_number_to_submenu


async def get_all_submenu(request: Request,
                          api_test_menu_id: uuid.UUID,
                          session: AsyncSession,
                          r: Redis):
    redis: RedisDAO = RedisDAO(r)
    data = redis.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)
    menu = await MC.get_menu_by_id(api_test_menu_id, session)
    if menu:
        submenus: list[BaseSubmenu] | None = menu.submenu
        if submenus:
            for elem in submenus:
                await add_dish_number_to_submenu(elem, session)
        redis.set(key=request.url.path + request.method, value=pickle.dumps(submenus),
                  expire_time=settings.REDIS_EXPIRE_TIME)
        return submenus
    else:
        return []


async def get_submenu_by_id(request: Request,
                            api_test_submenu_id: uuid.UUID,
                            session: AsyncSession,
                            r: Redis):
    redis: RedisDAO = RedisDAO(r)
    data = redis.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)

    submenu: SubmenuSchema | None = await SC.get_submenu_by_id(api_test_submenu_id, session)
    if submenu:
        await add_dish_number_to_submenu(submenu, session)
        redis.set(key=request.url.path + request.method, value=pickle.dumps(submenu),
                  expire_time=settings.REDIS_EXPIRE_TIME)
        return submenu
    else:
        raise HTTPException(status_code=404, detail='submenu not found')


async def create_submenu(request: Request,
                         api_test_menu_id: uuid.UUID,
                         submenu: CreateSubmenu,
                         session: AsyncSession,
                         r: Redis):
    redis: RedisDAO = RedisDAO(r)
    created_submenu: SubmenuSchema | None = await SC.create_submenu(api_test_menu_id, submenu, session)
    await add_dish_number_to_submenu(created_submenu, session)
    redis.unvalidate(request.url.path + 'GET',
                     '/api/v1/menus/' + str(api_test_menu_id) + 'GET',
                     '/api/v1/menusGET')
    return created_submenu


async def update_submenu_by_id(request: Request,
                               api_test_menu_id: uuid.UUID,
                               api_test_submenu_id: uuid.UUID,
                               submenu: CreateSubmenu,
                               session: AsyncSession,
                               r: Redis):
    redis: RedisDAO = RedisDAO(r)
    submenu_id: uuid.UUID | None = await SC.update_submenu_by_id(api_test_menu_id, api_test_submenu_id, submenu,
                                                                 session)
    if submenu_id:
        reterned_submenu: SubmenuSchema | None = await SC.get_submenu_by_id(submenu_id, session)
        if reterned_submenu:
            # print(reterned_submenu)
            await add_dish_number_to_submenu(reterned_submenu, session)
            redis.unvalidate(request.url.path + 'GET',
                             '/api/v1/menus/' + str(api_test_menu_id) + '/submenus' + 'GET',
                             '/api/v1/menus/' + str(api_test_menu_id) + 'GET',
                             '/api/v1/menusGET')
            return reterned_submenu
    else:
        raise HTTPException(status_code=404, detail='submenu not found')


async def delete_submenu_by_id(request: Request,
                               target_menu_id: uuid.UUID,
                               target_submenu_id: uuid.UUID,
                               session: AsyncSession,
                               r: Redis):
    redis: RedisDAO = RedisDAO(r)
    submenu = await SC.delete_submenu_by_id(target_submenu_id, session)
    if submenu:
        redis.unvalidate(request.url.path + 'GET',
                         '/api/v1/menus/' + str(target_menu_id) + '/submenus' + 'GET',
                         '/api/v1/menus/' + str(target_menu_id) + 'GET',
                         '/api/v1/menusGET')
        return {'status': True,
                'message': 'The submenu has been deleted'}
    else:
        raise HTTPException(status_code=404, detail='submenu not found')
