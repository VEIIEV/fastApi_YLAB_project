import uuid

from fastapi import APIRouter, Depends
from redis.client import Redis
from sqlalchemy.orm import Session
from starlette.requests import Request

from python_code.db import get_session
from python_code.redis import get_redis_connection
from python_code.schemas.submenu_schemas import CreateSubmenu
from python_code.service.submenu_service import (
    create_submenu,
    delete_submenu_by_id,
    get_all_submenu,
    get_submenu_by_id,
    update_submenu_by_id,
)

router = APIRouter(
    tags=['submenu'],
    responses={404: {'details': 'Submenu not found'}},
)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus')
def get_all_submenu_endpoint(request: Request,
                             api_test_menu_id: uuid.UUID,
                             session: Session = Depends(get_session),
                             r: Redis = Depends(get_redis_connection)):
    return get_all_submenu(request, api_test_menu_id, session, r)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def get_submenu_by_id_endpoint(request: Request,
                               api_test_submenu_id: uuid.UUID,
                               session: Session = Depends(get_session),
                               r: Redis = Depends(get_redis_connection)):
    return get_submenu_by_id(request, api_test_submenu_id, session, r)


@router.post('/api/v1/menus/{api_test_menu_id}/submenus', status_code=201)
def create_submenu_endpoint(request: Request,
                            api_test_menu_id: uuid.UUID,
                            submenu: CreateSubmenu,
                            session: Session = Depends(get_session),
                            r: Redis = Depends(get_redis_connection)):
    return create_submenu(request, api_test_menu_id, submenu, session, r)


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def update_submenu_by_id_endpoint(request: Request,
                                  api_test_menu_id: uuid.UUID,
                                  api_test_submenu_id: uuid.UUID,
                                  submenu: CreateSubmenu,
                                  session: Session = Depends(get_session),
                                  r: Redis = Depends(get_redis_connection)):
    return update_submenu_by_id(request, api_test_menu_id, api_test_submenu_id, submenu, session, r)


@router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def delete_submenu_by_id_endpoint(request: Request,
                                  target_menu_id: uuid.UUID,
                                  target_submenu_id: uuid.UUID,
                                  session: Session = Depends(get_session),
                                  r: Redis = Depends(get_redis_connection)):
    return delete_submenu_by_id(request, target_menu_id, target_submenu_id, session, r)
