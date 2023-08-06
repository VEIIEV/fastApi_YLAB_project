import pickle
import uuid
from typing import Sequence

from fastapi import HTTPException
from redis.client import Redis
from sqlalchemy.orm import Session
from starlette.requests import Request

from python_code.cruds import menu_crud as MC
from python_code.models.menu_model import Menu
from python_code.schemas.menu_schemas import CreateMenu, MenuSchema
from python_code.utils import add_counters_to_response


def find_all_menu(r: Redis,
                  request: Request,
                  session: Session):
    data = r.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)
    menu: Sequence[Menu] = MC.get_menu_all(session)
    for elem in menu:
        add_counters_to_response(elem, session)
    r.set(request.url.path + request.method, pickle.dumps(menu))
    r.expire(request.url.path + request.method, 180)
    return menu


def find_menu_by_id(r: Redis,
                    request: Request,
                    session: Session,
                    api_test_menu_id: uuid.UUID):
    data = r.get(request.url.path + request.method)
    if data:
        return pickle.loads(data)
    menu = MC.get_menu_by_id(api_test_menu_id, session)
    if menu:
        add_counters_to_response(menu, session)
        r.set(request.url.path + request.method, pickle.dumps(menu))
        r.expire(request.url.path + request.method, 180)
        return menu
    else:
        raise HTTPException(status_code=404, detail='menu not found')


def create_menu(menu: CreateMenu,
                r: Redis,
                request: Request,
                session: Session):
    r.delete(request.url.path + 'GET')
    created_menu: MenuSchema | None = MC.create_menu(menu, session)
    add_counters_to_response(created_menu, session)
    return created_menu


def update_menu_by_id(menu: CreateMenu,
                      api_test_menu_id: uuid.UUID,
                      r: Redis,
                      request: Request,
                      session: Session):
    menu_id: uuid.UUID | None = MC.update_menu_by_id(api_test_menu_id, menu, session)
    if menu_id:
        created_menu: MenuSchema | None = MC.get_menu_by_id(menu_id, session)
        add_counters_to_response(created_menu, session)
        r.delete(request.url.path + 'GET',
                 '/api/v1/menusGET')
        return created_menu
    else:
        raise HTTPException(status_code=404, detail='menu not found')


def delete_menu_by_id(request: Request,
                      api_test_menu_id: uuid.UUID,
                      session: Session,
                      r: Redis):
    menu_id = MC.delete_menu_by_id(api_test_menu_id, session)
    if menu_id:
        r.delete(request.url.path + 'GET',
                 '/api/v1/menusGET')
        return {'status': True,
                'message': 'The menu has been deleted'}
    else:
        raise HTTPException(status_code=404, detail='menu not found')
