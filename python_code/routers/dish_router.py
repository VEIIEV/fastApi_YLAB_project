import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Path
from redis.client import Redis
from sqlalchemy.orm import Session
from starlette.requests import Request

from python_code.cruds import dish_crud as DC
from python_code.db import get_session
from python_code.redis import get_redis_connection
from python_code.schemas.dish_schemas import CreateDish
from python_code.service.dish_service import (
    create_dish,
    delete_dish,
    get_all_dishes,
    get_dish_by_id,
    update_dish,
)

router = APIRouter(tags=['dish'],
                   responses={404: {'details': 'dish not found'}})


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes')
def get_all_dishes_endpoint(request: Request,
                            api_test_submenu_id: uuid.UUID,
                            session: Session = Depends(get_session),
                            r: Redis = Depends(get_redis_connection)):
    return get_all_dishes(request, api_test_submenu_id, session, r)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def get_dish_by_id_endpoint(request: Request,
                            api_test_dish_id: uuid.UUID,
                            session: Session = Depends(get_session),
                            r: Redis = Depends(get_redis_connection)):
    return get_dish_by_id(request, api_test_dish_id, session, r)


@router.post('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes', status_code=201)
def create_dish_endpoint(request: Request,
                         api_test_menu_id: uuid.UUID,
                         api_test_submenu_id: uuid.UUID,
                         dish: CreateDish,
                         session: Session = Depends(get_session),
                         r: Redis = Depends(get_redis_connection)):
    return create_dish(request, api_test_menu_id, api_test_submenu_id, dish, session, r)


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def update_dish_endpoint(request: Request,
                         api_test_menu_id: uuid.UUID,
                         api_test_submenu_id: uuid.UUID,
                         api_test_dish_id: uuid.UUID,
                         dish: CreateDish,
                         session: Session = Depends(get_session),
                         r: Redis = Depends(get_redis_connection)):
    return update_dish(request, api_test_menu_id, api_test_submenu_id, api_test_dish_id, dish, session, r)


@router.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def delete_dish_endpoint(request: Request,
                         api_test_menu_id: uuid.UUID,
                         api_test_submenu_id: uuid.UUID,
                         api_test_dish_id: uuid.UUID,
                         session: Session = Depends(get_session),
                         r: Redis = Depends(get_redis_connection)):
    return delete_dish(request, api_test_menu_id, api_test_submenu_id, api_test_dish_id, session, r)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/check/{title}')
def check_dish_existence(title: Annotated[str, Path(title='The ID of the item to get')],
                         session: Session = Depends(get_session)):
    return DC.is_exist_dish(title, session)
