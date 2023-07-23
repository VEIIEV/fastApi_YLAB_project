import uuid

import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import Session

from python_code.models.dish_model import Dish
from python_code.models.menu_model import Menu
from python_code.models.submenu_model import Submenu
from python_code.schemas.menu_schemas import MenuSchema, CreateMenu


def get_menu_all(session: Session):
    result = session.execute(sa.select(Menu))
    return result.scalars().all()


def get_menu_by_id(id: uuid.UUID, session: Session) -> MenuSchema:
    result = session.execute(sa.select(Menu).where(Menu.id == id))
    return result.scalar()


def create_menu(menu: CreateMenu, session: Session) -> MenuSchema:
    created_menu = session.execute(sa.insert(Menu).returning(Menu),
                                   [{'title': menu.title, 'description': menu.description}])
    session.commit()
    return created_menu.scalar()


def update_menu_by_id(menu_id: uuid.UUID, menu: CreateMenu, session: Session) -> uuid.UUID:
    updated_menu = session.connection().execute(
        sa.update(Menu).where(Menu.id == menu_id).returning(Menu),
        [{'title': menu.title, 'description': menu.description}])
    session.commit()
    return updated_menu.scalar()


def delete_menu_by_id(id: uuid.UUID, session: Session) -> MenuSchema:
    deleted_menu = session.execute(sa.delete(Menu).returning(Menu).where(Menu.id == id))
    session.commit()
    return deleted_menu.scalar()


def count_submenu(menu_id: uuid.UUID, session: Session) -> int:
    result = session.execute(sa.select(func.count(Submenu.id)).join(Menu.submenu).where(Menu.id == menu_id))
    return result.scalar()


def count_dishes(menu_id: uuid.UUID, session: Session) -> int:
    result = session.execute(
        sa.select(func.count(Dish.id))
        .join(Menu.submenu)
        .join(Submenu.dishes)
        .where(Menu.id == menu_id))
    return result.scalar()
