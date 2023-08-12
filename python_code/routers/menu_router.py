import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from redis.asyncio.client import Redis  # type ignore[import]"
from sqlalchemy.ext.asyncio import AsyncSession

from python_code.db import get_async_session
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


@router.get('/api/v1/menus',
            summary='get all menu',
            response_description='list of all menu, if empty return []')
async def get_all_menu_endpoint(request: Request,
                                session: AsyncSession = Depends(get_async_session),
                                r: Redis = Depends(get_redis_connection)):
    """
    Return dishes with all the information:
    - **title**:
    - **description**:
    - **own_id**:
    - **submenu's list**:
    """
    return await find_all_menu(r, request, session)


@router.get('/api/v1/menus/{api_test_menu_id}',
            summary='return menu with pointed id', )
async def get_menu_by_id_endpoint(request: Request,
                                  api_test_menu_id: uuid.UUID,
                                  session: AsyncSession = Depends(get_async_session),
                                  r: Redis = Depends(get_redis_connection)):
    """
    Return selected menu if existed, else return 404:
    - **title**:
    - **description**:
    - **own_id**:
    - **submenu's list**:
    """
    return await find_menu_by_id(r, request, session, api_test_menu_id)


@router.post('/api/v1/menus', status_code=201,
             summary='create menu')
async def create_menu_endpoint(request: Request,
                               menu: CreateMenu,
                               background_tasks: BackgroundTasks,
                               session: AsyncSession = Depends(get_async_session),
                               r: Redis = Depends(get_redis_connection)):
    """
    Create new menu and return  created menu data
    - **title**:
    - **description**:
    - **own_id**:
    - **submenu's list**:
    """
    return await create_menu(menu, r, request, session, background_tasks)


@router.patch('/api/v1/menus/{api_test_menu_id}',
              summary='update menu')
async def update_menu_by_id_endpoint(request: Request,
                                     api_test_menu_id: uuid.UUID,
                                     menu: CreateMenu,
                                     background_tasks: BackgroundTasks,
                                     session: AsyncSession = Depends(get_async_session),
                                     r: Redis = Depends(get_redis_connection)):
    """
    if exist Update menu and return  updated menu data
    else return 404:
    - **title**:
    - **description**:
    - **own_id**:
    - **submenu's list**:
    """
    return await update_menu_by_id(menu, api_test_menu_id, r, request, session, background_tasks)


@router.delete('/api/v1/menus/{api_test_menu_id}',
               summary='delete menu')
async def delete_menu_by_id_endpoint(request: Request,
                                     api_test_menu_id: uuid.UUID,
                                     background_tasks: BackgroundTasks,
                                     session: AsyncSession = Depends(get_async_session),
                                     r: Redis = Depends(get_redis_connection)):
    """
    if exist delete selected menu and return confirm message
    else return 404
    """
    return await delete_menu_by_id(request, api_test_menu_id, session, r, background_tasks)
