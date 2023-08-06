import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from python_code.cruds import menu_crud as MC
from python_code.db import get_session
from python_code.schemas.menu_schemas import CreateMenu

router = APIRouter(
    tags=['menu'],
    responses={404: {'details': 'Menu not found'}},
)


def add_counters_to_response(menu, session):
    'Util func that add counter of dish and sub to menu resp'

    submenus_count = MC.count_submenu(menu.id, session)
    dishes_count = MC.count_dishes(menu.id, session)
    menu.__setattr__('submenus_count', submenus_count)
    menu.__setattr__('dishes_count', dishes_count)


@router.get('/api/v1/menus')
def get_all_menu(session: Session = Depends(get_session)):
    menu = MC.get_menu_all(session)
    for elem in menu:
        add_counters_to_response(elem, session)
    return menu


@router.get('/api/v1/menus/{api_test_menu_id}')
def get_menu_by_id(api_test_menu_id: uuid.UUID, session: Session = Depends(get_session)):
    menu = MC.get_menu_by_id(api_test_menu_id, session)
    if menu:
        add_counters_to_response(menu, session)
    else:
        raise HTTPException(status_code=404, detail='menu not found')
    return menu


@router.post('/api/v1/menus', status_code=201)
def create_menu(menu: CreateMenu, session: Session = Depends(get_session)):
    menu = MC.create_menu(menu, session)
    add_counters_to_response(menu, session)
    return menu


@router.patch('/api/v1/menus/{api_test_menu_id}')
def update_menu_by_id(api_test_menu_id: uuid.UUID, menu: CreateMenu, session: Session = Depends(get_session)):
    menu_id = MC.update_menu_by_id(api_test_menu_id, menu, session)
    if menu_id:
        menu = MC.get_menu_by_id(menu_id, session)
        # print(menu)
        add_counters_to_response(menu, session)
    else:
        raise HTTPException(status_code=404, detail='menu not found')

    return menu


@router.delete('/api/v1/menus/{api_test_menu_id}')
def delete_menu_by_id(api_test_menu_id: uuid.UUID, session: Session = Depends(get_session)):
    menu_id = MC.delete_menu_by_id(api_test_menu_id, session)
    if menu_id:
        print(menu_id.id)
        return {'status': True,
                'message': 'The menu has been deleted'}
    else:
        raise HTTPException(status_code=404, detail='menu not found')
