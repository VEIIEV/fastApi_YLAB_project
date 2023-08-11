import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from redis.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from python_code.cruds import dish_crud as DC
from python_code.db import get_async_session
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


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes',
            summary='gets all dishes belonging to submenu that specified in url',
            response_description='list of all dishes, if empty return: []')
async def get_all_dishes_endpoint(request: Request,
                                  api_test_submenu_id: uuid.UUID,
                                  session: AsyncSession = Depends(get_async_session),
                                  r: Redis = Depends(get_redis_connection)):
    """
    Return dishes with all the information:

    - **title**:
    - **description**:
    - **price**:  rounded to .2f
    - **own_id**:
    - **submenu_id**:
    """
    return await get_all_dishes(request, api_test_submenu_id, session, r)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}',
            summary='return dish with pointed id')
async def get_dish_by_id_endpoint(request: Request,
                                  api_test_dish_id: uuid.UUID,
                                  session: AsyncSession = Depends(get_async_session),
                                  r: Redis = Depends(get_redis_connection)):
    """
    Return selected dish if existed, else return 404:
    - **title**:
    - **description**:
    - **price**:  rounded to .2f
    - **own_id**:
    - **submenu_id**:
    """
    return await get_dish_by_id(request, api_test_dish_id, session, r)


@router.post('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes', status_code=201,
             summary='create dish in pointed submenu')
async def create_dish_endpoint(request: Request,
                               api_test_menu_id: uuid.UUID,
                               api_test_submenu_id: uuid.UUID,
                               session: AsyncSession = Depends(get_async_session),
                               r: Redis = Depends(get_redis_connection),
                               dish: CreateDish = Body(example={
                                   'title': 'food',
                                   'description': 'amazing food fow your maws',
                                   'price': '645.32'
                               })):
    """
    Create new dish in selected submenu and return  created dish data
    - **title**:
    - **description**:
    - **price**:  rounded to .2f
    - **own_id**:
    - **submenu_id**:
    """
    return await create_dish(request, api_test_menu_id, api_test_submenu_id, dish, session, r)


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}',
              summary='update dish in pointed submenu')
async def update_dish_endpoint(request: Request,
                               api_test_menu_id: uuid.UUID,
                               api_test_submenu_id: uuid.UUID,
                               api_test_dish_id: uuid.UUID,
                               dish: CreateDish,
                               session: AsyncSession = Depends(get_async_session),
                               r: Redis = Depends(get_redis_connection)):
    """
    if exist Update dish in selected submenu and return  updated dish data
    else return 404
    - **title**:
    - **description**:
    - **price**:  rounded to .2f
    - **own_id**:
    - **submenu_id**:
    """
    return await update_dish(request, api_test_menu_id, api_test_submenu_id, api_test_dish_id, dish, session, r)


@router.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}',
               summary='delete pointed dish')
async def delete_dish_endpoint(request: Request,
                               api_test_menu_id: uuid.UUID,
                               api_test_submenu_id: uuid.UUID,
                               api_test_dish_id: uuid.UUID,
                               session: AsyncSession = Depends(get_async_session),
                               r: Redis = Depends(get_redis_connection)):
    """
    if exist delete selected dish and return confirm message
    else return 404
    """
    return await delete_dish(request, api_test_menu_id, api_test_submenu_id, api_test_dish_id, session, r)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/check/{title}',
            summary='check dish existance by titile')
async def check_dish_existence(title: Annotated[str, Path(title='The ID of the item to get')],
                               session: AsyncSession = Depends(get_async_session), ):
    """
    get dish title and return exist that dish or not
    """
    return await DC.is_exist_dish(title, session)
