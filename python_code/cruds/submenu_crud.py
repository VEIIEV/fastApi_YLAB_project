import uuid
from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from python_code.models.dish_model import Dish
from python_code.models.submenu_model import Submenu
from python_code.schemas.submenu_schemas import CreateSubmenu, SubmenuSchema


def get_submenu_all(session: Session) -> Sequence[SubmenuSchema]:
    result = session.execute(sa.select(SubmenuSchema))
    return result.scalars().all()


def get_submenu_by_id(id: uuid.UUID, session: Session) -> SubmenuSchema | None:
    result = session.execute(sa.select(Submenu).where(Submenu.id == id))
    return result.scalar()


def create_submenu(menu_id: uuid.UUID, submenu: CreateSubmenu, session: Session) -> SubmenuSchema:
    created_submenu = session.execute(sa.insert(Submenu).returning(Submenu),
                                      [{'title': submenu.title,
                                        'description': submenu.description,
                                        'menu_id': menu_id}])
    session.commit()
    return created_submenu.scalar()


def update_submenu_by_id(menu_id: uuid.UUID, submenu_id: uuid.UUID, submenu: CreateSubmenu,
                         session: Session) -> uuid.UUID | None:
    updated_submenu = session.connection().execute(
        sa.update(Submenu).where(Submenu.id == submenu_id).returning(Submenu),
        [{'title': submenu.title,
          'description': submenu.description,
          'menu_id': menu_id}])
    session.commit()
    return updated_submenu.scalar()


def delete_submenu_by_id(id: uuid.UUID, session: Session) -> SubmenuSchema:
    deleted_submenu = session.execute(sa.delete(Submenu).returning(Submenu).where(Submenu.id == id))
    session.commit()
    return deleted_submenu.scalar()


def count_dishes(submenu_id: uuid.UUID, session: Session) -> int:
    result = session.execute(
        sa.select(func.count(Dish.id))
        .join(Submenu.dishes)
        .where(Submenu.id == submenu_id))
    return result.scalar()
