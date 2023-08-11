import pickle
import uuid

from fastapi import HTTPException
from redis.client import Redis
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from python_code.config import settings
from python_code.cruds import dish_crud as DC
from python_code.dao.redis_dao import RedisDAO
from python_code.schemas.dish_schemas import CreateDish, DishSchema
from python_code.utils import round_price


async def get_all_dishes(request: Request,
                         api_test_submenu_id: uuid.UUID,
                         session: AsyncSession,
                         r: Redis):
    redis: RedisDAO = RedisDAO(r)
    data = redis.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)

    dishes: Sequence[DishSchema] = await DC.get_dish_for_submenu_all(api_test_submenu_id, session)
    if dishes:
        for dish in dishes:
            round_price(dish)
    redis.set(key=request.url.path + request.method, value=pickle.dumps(dishes),
              expire_time=settings.REDIS_EXPIRE_TIME)
    return dishes


async def get_dish_by_id(request: Request,
                         api_test_dish_id: uuid.UUID,
                         session: AsyncSession,
                         r: Redis):
    redis: RedisDAO = RedisDAO(r)
    data = redis.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)

    dish = await DC.get_dish_by_id(api_test_dish_id, session)
    if dish:
        round_price(dish)
        redis.set(key=request.url.path + request.method, value=pickle.dumps(dish),
                  expire_time=settings.REDIS_EXPIRE_TIME)
        return dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


async def create_dish(request: Request,
                      api_test_menu_id: uuid.UUID,
                      api_test_submenu_id: uuid.UUID,
                      dish: CreateDish,
                      session: AsyncSession,
                      r: Redis):
    redis: RedisDAO = RedisDAO(r)
    returned_dish: DishSchema | None = await DC.create_dish(api_test_submenu_id, dish, session)
    if returned_dish:
        round_price(returned_dish)
        redis.unvalidate(request.url.path + 'GET',
                         '/api/v1/menus/' + str(api_test_menu_id) + '/submenus/' + str(api_test_submenu_id) + 'GET',
                         '/api/v1/menus/' + str(api_test_menu_id) + '/submenus' + 'GET',
                         '/api/v1/menus/' + str(api_test_menu_id) + 'GET',
                         '/api/v1/menusGET')
        return returned_dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


async def update_dish(request: Request,
                      api_test_menu_id: uuid.UUID,
                      api_test_submenu_id: uuid.UUID,
                      api_test_dish_id: uuid.UUID,
                      dish: CreateDish,
                      session: AsyncSession,
                      r: Redis):
    redis: RedisDAO = RedisDAO(r)
    dish_id = await DC.update_dish_by_id(api_test_submenu_id, api_test_dish_id, dish, session)
    if dish_id:
        updated_dish: DishSchema | None = await DC.get_dish_by_id(dish_id, session)
        round_price(updated_dish)
        redis.unvalidate(request.url.path + 'GET',
                         '/api/v1/menus/' + str(api_test_menu_id) + '/submenus/' + str(
                             api_test_submenu_id) + '/dishes' + 'GET',
                         '/api/v1/menus/' + str(api_test_menu_id) + '/submenus/' + str(api_test_submenu_id) + 'GET',
                         '/api/v1/menus/' + str(api_test_menu_id) + '/submenus' + 'GET',
                         '/api/v1/menus/' + str(api_test_menu_id) + 'GET',
                         '/api/v1/menusGET')
        return updated_dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


async def delete_dish(request: Request,
                      api_test_menu_id: uuid.UUID,
                      api_test_submenu_id: uuid.UUID,
                      api_test_dish_id: uuid.UUID,
                      session: AsyncSession,
                      r: Redis):
    redis: RedisDAO = RedisDAO(r)
    dish = await DC.delete_dish_by_id(api_test_dish_id, session)
    if dish:
        redis.unvalidate(request.url.path + 'GET',
                         '/api/v1/menus/' + str(api_test_menu_id) + '/submenus/' + str(
                             api_test_submenu_id) + '/dishes' + 'GET',
                         '/api/v1/menus/' + str(api_test_menu_id) + '/submenus/' + str(api_test_submenu_id) + 'GET',
                         '/api/v1/menus/' + str(api_test_menu_id) + '/submenus' + 'GET',
                         '/api/v1/menus/' + str(api_test_menu_id) + 'GET',
                         '/api/v1/menusGET')
        return {'status': True,
                'message': 'The dish has been deleted'}
    else:
        raise HTTPException(status_code=404, detail='dish not found')
