import uuid

from fastapi import APIRouter, Depends
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from python_code.db import get_async_session
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


@router.get('/api/v1/menus/{api_test_menu_id}/submenus',
            summary='get all submenu belonging to menu that specified in url',
            response_description='list of all submenu, if empty return []')
async def get_all_submenu_endpoint(request: Request,
                                   api_test_menu_id: uuid.UUID,
                                   session: AsyncSession = Depends(get_async_session),
                                   r: Redis = Depends(get_redis_connection)):
    """
    Return submenu with all the information:
    - **title**:
    - **description**:
    """
    return await get_all_submenu(request, api_test_menu_id, session, r)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}',
            summary='return submenu with pointed id', )
async def get_submenu_by_id_endpoint(request: Request,
                                     api_test_submenu_id: uuid.UUID,
                                     session: AsyncSession = Depends(get_async_session),
                                     r: Redis = Depends(get_redis_connection)):
    """
    Return selected submenu if existed, else return 404:
    - **title**:
    - **description**:
    - **own_id**:
    - **dishes_list**:
    - **menu_id**
    """
    return await get_submenu_by_id(request, api_test_submenu_id, session, r)


@router.post('/api/v1/menus/{api_test_menu_id}/submenus', status_code=201,
             summary='create submenu in pointed menu')
async def create_submenu_endpoint(request: Request,
                                  api_test_menu_id: uuid.UUID,
                                  submenu: CreateSubmenu,
                                  session: AsyncSession = Depends(get_async_session),
                                  r: Redis = Depends(get_redis_connection)):
    """
    Create new submenu in selected menu and return created submenu data
    - **title**:
    - **description**:
    - **own_id**:
    - **dishes_list**:
    - **menu_id**
    """
    return await create_submenu(request, api_test_menu_id, submenu, session, r)


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}',
              summary='update submenu in pointed menu')
async def update_submenu_by_id_endpoint(request: Request,
                                        api_test_menu_id: uuid.UUID,
                                        api_test_submenu_id: uuid.UUID,
                                        submenu: CreateSubmenu,
                                        session: AsyncSession = Depends(get_async_session),
                                        r: Redis = Depends(get_redis_connection)):
    """
    if exist Update submenu in selected menu and return updated submenu data
    else return 404
    - **title**:
    - **description**:
    - **own_id**:
    - **dishes_list**:
    - **menu_id**
    """
    return await update_submenu_by_id(request, api_test_menu_id, api_test_submenu_id, submenu, session, r)


@router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}',
               summary='delete pointed submenu')
async def delete_submenu_by_id_endpoint(request: Request,
                                        target_menu_id: uuid.UUID,
                                        target_submenu_id: uuid.UUID,
                                        session: AsyncSession = Depends(get_async_session),
                                        r: Redis = Depends(get_redis_connection)):
    """
    if exist delete selected submenu and return confirm message
    else return 404
    """
    return await delete_submenu_by_id(request, target_menu_id, target_submenu_id, session, r)
