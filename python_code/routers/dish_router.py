import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from python_code.cruds import dish_crud as DC
from python_code.db import get_session
from python_code.schemas.dish_schemas import CreateDish, DishSchema
from python_code.utils import round_price

router = APIRouter(tags=['dish'],
                   responses={404: {'details': 'dish not found'}})


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes')
def get_all_dishes(api_test_submenu_id: uuid.UUID, session: Session = Depends(get_session)):
    dishes: Sequence[DishSchema] = DC.get_dish_for_submenu_all(api_test_submenu_id, session)
    if dishes:
        for dish in dishes:
            round_price(dish)
    return dishes


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def get_dish_by_id(api_test_dish_id: uuid.UUID, session: Session = Depends(get_session)):
    dish = DC.get_dish_by_id(api_test_dish_id, session)
    if dish:
        round_price(dish)
        return dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


@router.post('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes', status_code=201)
def create_dish(api_test_submenu_id: uuid.UUID,
                dish: CreateDish,
                session: Session = Depends(get_session)):
    returned_dish: DishSchema | None = DC.create_dish(api_test_submenu_id, dish, session)
    if returned_dish:
        round_price(returned_dish)
        return returned_dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def update_dish(api_test_submenu_id: uuid.UUID,
                api_test_dish_id: uuid.UUID,
                dish: CreateDish,
                session: Session = Depends(get_session)):
    dish_id = DC.update_dish_by_id(api_test_submenu_id, api_test_dish_id, dish, session)
    if dish_id:
        updated_dish: DishSchema | None = DC.get_dish_by_id(dish_id, session)
        round_price(updated_dish)
        return updated_dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


@router.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def delete_dish(api_test_dish_id: uuid.UUID, session: Session = Depends(get_session)):
    dish = DC.delete_dish_by_id(api_test_dish_id, session)
    if dish:
        return {'status': True,
                'message': 'The dish has been deleted'}
    else:
        raise HTTPException(status_code=404, detail='dish not found')


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/check/{title}')
def check_dish_existence(title: Annotated[str, Path(title='The ID of the item to get')],
                         session: Session = Depends(get_session)):
    return DC.is_exist_dish(title, session)
