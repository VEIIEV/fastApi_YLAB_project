import uuid

from fastapi import APIRouter, Depends, Request
from redis.client import Redis  # type ignore[import]"
from sqlalchemy.orm import Session

from python_code.db import get_session
from python_code.redis import get_redis_connection
from python_code.schemas.menu_schemas import CreateMenu
from python_code.service.menu_service import (
    create_menu,
    delete_menu_by_id,
    find_all_menu,
    find_menu_by_id,
    update_menu_by_id,
)

router = APIRouter(
    tags=['menu'],
    responses={404: {'details': 'Menu not found'}},
)


@router.get('/api/v1/menus')
def get_all_menu_endpoint(request: Request,
                          session: Session = Depends(get_session),
                          r: Redis = Depends(get_redis_connection)):
    return find_all_menu(r, request, session)


@router.get('/api/v1/menus/{api_test_menu_id}')
def get_menu_by_id_endpoint(request: Request,
                            api_test_menu_id: uuid.UUID,
                            session: Session = Depends(get_session),
                            r: Redis = Depends(get_redis_connection)):
    return find_menu_by_id(r, request, session, api_test_menu_id)


@router.post('/api/v1/menus', status_code=201)
def create_menu_endpoint(request: Request,
                         menu: CreateMenu,
                         session: Session = Depends(get_session),
                         r: Redis = Depends(get_redis_connection)):
    return create_menu(menu, r, request, session)


@router.patch('/api/v1/menus/{api_test_menu_id}')
def update_menu_by_id_endpoint(request: Request,
                               api_test_menu_id: uuid.UUID,
                               menu: CreateMenu,
                               session: Session = Depends(get_session),
                               r: Redis = Depends(get_redis_connection)):
    return update_menu_by_id(menu, api_test_menu_id, r, request, session)


@router.delete('/api/v1/menus/{api_test_menu_id}')
def delete_menu_by_id_endpoint(request: Request,
                               api_test_menu_id: uuid.UUID,
                               session: Session = Depends(get_session),
                               r: Redis = Depends(get_redis_connection)):
    return delete_menu_by_id(request, api_test_menu_id, session, r)
