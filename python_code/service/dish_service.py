import pickle
import uuid

from fastapi import HTTPException
from redis.client import Redis
from sqlalchemy import Sequence
from sqlalchemy.orm import Session
from starlette.requests import Request

from python_code.cruds import dish_crud as DC
from python_code.schemas.dish_schemas import CreateDish, DishSchema
from python_code.utils import round_price


def get_all_dishes(request: Request,
                   api_test_submenu_id: uuid.UUID,
                   session: Session,
                   r: Redis):
    data = r.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)

    dishes: Sequence[DishSchema] = DC.get_dish_for_submenu_all(api_test_submenu_id, session)
    if dishes:
        for dish in dishes:
            round_price(dish)
    r.set(request.url.path + request.method, pickle.dumps(dishes))
    r.expire(request.url.path + request.method, 60)
    return dishes


def get_dish_by_id(request: Request,
                   api_test_dish_id: uuid.UUID,
                   session: Session,
                   r: Redis):
    data = r.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)

    dish = DC.get_dish_by_id(api_test_dish_id, session)
    if dish:
        round_price(dish)
        r.set(request.url.path + request.method, pickle.dumps(dish))
        r.expire(request.url.path + request.method, 60)
        return dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


def create_dish(request: Request,
                api_test_menu_id: uuid.UUID,
                api_test_submenu_id: uuid.UUID,
                dish: CreateDish,
                session: Session,
                r: Redis):
    returned_dish: DishSchema | None = DC.create_dish(api_test_submenu_id, dish, session)
    if returned_dish:
        round_price(returned_dish)
        r.delete(request.url.path + 'GET',
                 '/api/v1/menus/' + str(api_test_menu_id) + '/submenus/' + str(api_test_submenu_id) + 'GET',
                 '/api/v1/menus/' + str(api_test_menu_id) + '/submenus' + 'GET',
                 '/api/v1/menus/' + str(api_test_menu_id) + 'GET',
                 '/api/v1/menusGET')
        return returned_dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


def update_dish(request: Request,
                api_test_menu_id: uuid.UUID,
                api_test_submenu_id: uuid.UUID,
                api_test_dish_id: uuid.UUID,
                dish: CreateDish,
                session: Session,
                r: Redis):
    dish_id = DC.update_dish_by_id(api_test_submenu_id, api_test_dish_id, dish, session)
    if dish_id:
        updated_dish: DishSchema | None = DC.get_dish_by_id(dish_id, session)
        round_price(updated_dish)
        r.delete(request.url.path + 'GET',
                 '/api/v1/menus/' + str(api_test_menu_id) + '/submenus/' + str(api_test_submenu_id) + '/dishes' + 'GET',
                 '/api/v1/menus/' + str(api_test_menu_id) + '/submenus/' + str(api_test_submenu_id) + 'GET',
                 '/api/v1/menus/' + str(api_test_menu_id) + '/submenus' + 'GET',
                 '/api/v1/menus/' + str(api_test_menu_id) + 'GET',
                 '/api/v1/menusGET')
        return updated_dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


def delete_dish(request: Request,
                api_test_menu_id: uuid.UUID,
                api_test_submenu_id: uuid.UUID,
                api_test_dish_id: uuid.UUID,
                session: Session,
                r: Redis):
    dish = DC.delete_dish_by_id(api_test_dish_id, session)
    if dish:
        r.delete(request.url.path + 'GET',
                 '/api/v1/menus/' + str(api_test_menu_id) + '/submenus/' + str(api_test_submenu_id) + '/dishes' + 'GET',
                 '/api/v1/menus/' + str(api_test_menu_id) + '/submenus/' + str(api_test_submenu_id) + 'GET',
                 '/api/v1/menus/' + str(api_test_menu_id) + '/submenus' + 'GET',
                 '/api/v1/menus/' + str(api_test_menu_id) + 'GET',
                 '/api/v1/menusGET')
        return {'status': True,
                'message': 'The dish has been deleted'}
    else:
        raise HTTPException(status_code=404, detail='dish not found')
