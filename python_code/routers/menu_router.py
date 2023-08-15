import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from redis.asyncio.client import Redis  # type ignore[import]"
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from python_code.db import get_async_session
from python_code.redis import get_redis_connection
from python_code.schemas.menu_schemas import CreateMenu
from python_code.service.menu_service import (
    create_menu,
    delete_menu_by_id,
    find_all_menu,
    find_menu_by_id,
    get_all_menu_expanded,
    update_menu_by_id,
)
from python_code.utils import read_excel, update_db_from_excel

router = APIRouter(
    tags=['menu'],
    responses={404: {'details': 'Menu not found'}},
)


# todo delete later
@router.get('/api/v1/menus/adb',
            summary='sync db with excel')
async def update_db():
    try:
        menus_data, submenus_data, dishes_data = read_excel()
        response = await update_db_from_excel(menus_data, submenus_data, dishes_data)
        print(response)
        return {'list of updated entities:\n': response}
    except IntegrityError:
        raise HTTPException(status_code=404,
                            detail='всё впорядке, но есть одно но, uuid генерируется сам собой, и он очевидно не будет совпадать '
                                   'с тем что находится в excel, если хотите что бы оно работало, заходите в excel и ручками прописывайте'
                                   'uuid для каждой созданной в бд менюшке'
                                   'потом для под менюшки, а потом все будет работать')


@router.get('/api/v1/menus/expanded',
            summary='get expanded info about all menu',
            response_description='The nested list that stores information about all dishes and dishes, '
                                 'if empty return []',
            )
async def get_all_menu_expanded_endpoint(request: Request,
                                         session: AsyncSession = Depends(get_async_session),
                                         r: Redis = Depends(get_redis_connection)):
    """
    Return nexted list with detail info about all menu
    """
    return await get_all_menu_expanded(r, request, session)


@router.get('/api/v1/menus',
            summary='get all menu',
            response_description='list of all menu, if empty return []')
async def get_all_menu_endpoint(request: Request,
                                session: AsyncSession = Depends(get_async_session),
                                r: Redis = Depends(get_redis_connection)):
    """
    Return list of menu with all the information:
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
