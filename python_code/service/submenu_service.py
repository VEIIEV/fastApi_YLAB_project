import pickle
import uuid

from fastapi import HTTPException
from redis.client import Redis
from sqlalchemy.orm import Session
from starlette.requests import Request

from python_code.cruds import menu_crud as MC
from python_code.cruds import submenu_crud as SC
from python_code.schemas.submenu_schemas import (
    BaseSubmenu,
    CreateSubmenu,
    SubmenuSchema,
)
from python_code.utils import add_dish_number_to_submenu


def get_all_submenu(request: Request,
                    api_test_menu_id: uuid.UUID,
                    session: Session,
                    r: Redis):
    data = r.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)
    menu = MC.get_menu_by_id(api_test_menu_id, session)
    if menu:
        submenus: list[BaseSubmenu] | None = menu.submenu
        if submenus:
            for elem in submenus:
                add_dish_number_to_submenu(session, elem)
        r.set(request.url.path + request.method, pickle.dumps(submenus))
        r.expire(request.url.path + request.method, 60)
        return submenus
    else:
        return []


def get_submenu_by_id(request: Request,
                      api_test_submenu_id: uuid.UUID,
                      session: Session,
                      r: Redis):
    data = r.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)

    submenu: SubmenuSchema | None = SC.get_submenu_by_id(api_test_submenu_id, session)
    if submenu:
        add_dish_number_to_submenu(session, submenu)
        r.set(request.url.path + request.method, pickle.dumps(submenu))
        r.expire(request.url.path + request.method, 60)
        return submenu
    else:
        raise HTTPException(status_code=404, detail='submenu not found')


def create_submenu(request: Request,
                   api_test_menu_id: uuid.UUID,
                   submenu: CreateSubmenu,
                   session: Session,
                   r: Redis):
    created_submenu: SubmenuSchema | None = SC.create_submenu(api_test_menu_id, submenu, session)
    add_dish_number_to_submenu(session, created_submenu)
    r.delete(request.url.path + 'GET',
             '/api/v1/menus/' + str(api_test_menu_id) + 'GET',
             '/api/v1/menusGET')
    return created_submenu


def update_submenu_by_id(request: Request,
                         api_test_menu_id: uuid.UUID,
                         api_test_submenu_id: uuid.UUID,
                         submenu: CreateSubmenu,
                         session: Session,
                         r: Redis):
    submenu_id: uuid.UUID | None = SC.update_submenu_by_id(api_test_menu_id, api_test_submenu_id, submenu, session)
    if submenu_id:
        reterned_submenu: SubmenuSchema | None = SC.get_submenu_by_id(submenu_id, session)
        if reterned_submenu:
            # print(reterned_submenu)
            add_dish_number_to_submenu(session, reterned_submenu)
            r.delete(request.url.path + 'GET',
                     '/api/v1/menus/' + str(api_test_menu_id) + '/submenus' + 'GET',
                     '/api/v1/menus/' + str(api_test_menu_id) + 'GET',
                     '/api/v1/menusGET')
            return reterned_submenu
    else:
        raise HTTPException(status_code=404, detail='submenu not found')


def delete_submenu_by_id(request: Request,
                         target_menu_id: uuid.UUID,
                         target_submenu_id: uuid.UUID,
                         session: Session,
                         r: Redis):
    submenu = SC.delete_submenu_by_id(target_submenu_id, session)
    if submenu:
        r.delete(request.url.path + 'GET',
                 '/api/v1/menus/' + str(target_menu_id) + '/submenus' + 'GET',
                 '/api/v1/menus/' + str(target_menu_id) + 'GET',
                 '/api/v1/menusGET')
        return {'status': True,
                'message': 'The submenu has been deleted'}
    else:
        raise HTTPException(status_code=404, detail='submenu not found')
