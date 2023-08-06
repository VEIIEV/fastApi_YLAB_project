import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from python_code.cruds import menu_crud as MC
from python_code.cruds import submenu_crud as SC
from python_code.db import get_session
from python_code.schemas.submenu_schemas import (
    BaseSubmenu,
    CreateSubmenu,
    SubmenuSchema,
)
from python_code.utils import add_dish_number_to_submenu

router = APIRouter(
    tags=['submenu'],
    responses={404: {'details': 'Submenu not found'}},
)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus')
def get_all_submenu(api_test_menu_id: uuid.UUID, session: Session = Depends(get_session)):
    menu = MC.get_menu_by_id(api_test_menu_id, session)
    if menu:
        submenus: list[BaseSubmenu] | None = menu.submenu
        if submenus:
            for elem in submenus:
                add_dish_number_to_submenu(session, elem)
    else:
        return []
    return submenus


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def get_submenu_by_id(api_test_submenu_id: uuid.UUID,
                      session: Session = Depends(get_session)):
    submenu: SubmenuSchema | None = SC.get_submenu_by_id(api_test_submenu_id, session)
    if submenu:
        add_dish_number_to_submenu(session, submenu)
    else:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenu


@router.post('/api/v1/menus/{api_test_menu_id}/submenus', status_code=201)
def create_submenu(api_test_menu_id: uuid.UUID,
                   submenu: CreateSubmenu,
                   session: Session = Depends(get_session)):
    created_submenu: SubmenuSchema | None = SC.create_submenu(api_test_menu_id, submenu, session)
    if created_submenu:
        add_dish_number_to_submenu(session, created_submenu)
    return created_submenu


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def update_submenu_by_id(api_test_menu_id: uuid.UUID,
                         api_test_submenu_id: uuid.UUID,
                         submenu: CreateSubmenu,
                         session: Session = Depends(get_session)):
    submenu_id: uuid.UUID | None = SC.update_submenu_by_id(api_test_menu_id, api_test_submenu_id, submenu, session)
    if submenu_id:
        reterned_submenu: SubmenuSchema | None = SC.get_submenu_by_id(submenu_id, session)
        if reterned_submenu:
            # print(reterned_submenu)
            add_dish_number_to_submenu(session, reterned_submenu)
            return reterned_submenu
    else:
        raise HTTPException(status_code=404, detail='submenu not found')


@router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def delete_submenu_by_id(target_submenu_id: uuid.UUID,
                         session: Session = Depends(get_session)):
    submenu = SC.delete_submenu_by_id(target_submenu_id, session)
    if submenu:
        # print(submenu.id)
        return {'status': True,
                'message': 'The submenu has been deleted'}
    else:
        raise HTTPException(status_code=404, detail='submenu not found')
