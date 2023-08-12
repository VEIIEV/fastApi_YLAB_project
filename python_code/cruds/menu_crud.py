import uuid
from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import func

from python_code.models.dish_model import Dish
from python_code.models.menu_model import Menu
from python_code.models.submenu_model import Submenu
from python_code.schemas.menu_schemas import CreateMenu, MenuExpandedSchema, MenuSchema


async def get_menu_all_expanded(session: AsyncSession) -> Sequence[MenuExpandedSchema]:
    result: AsyncResult = await session.execute(
        sa.select(Menu, Submenu, Dish)
        .outerjoin(Menu.submenu)
        .outerjoin(Submenu.dishes)
        .options(joinedload(Menu.submenu).joinedload(Submenu.dishes)))
    return result.unique().scalars().all()


async def get_menu_all(session: AsyncSession) -> Sequence[Menu]:
    result: AsyncResult = await session.execute(sa.select(Menu))

    return result.scalars().all()


async def get_menu_by_id(id: uuid.UUID, session: AsyncSession) -> MenuSchema | None:
    result: AsyncResult = await session.execute(sa.select(Menu).filter_by(id=id))
    return result.scalar()


async def create_menu(menu: CreateMenu, session: AsyncSession) -> MenuSchema | None:
    created_menu: AsyncResult = await session.execute(sa.insert(Menu).returning(Menu),
                                                      [{'title': menu.title, 'description': menu.description}])
    await session.commit()
    return created_menu.scalar()


# todo и тут тоже
async def update_menu_by_id(menu_id: uuid.UUID, menu: CreateMenu, session: AsyncSession):
    updated_menu: AsyncResult = await session.execute(
        sa.update(Menu).where(Menu.id == menu_id).returning(Menu).values(
            title=menu.title,
            description=menu.description))
    await session.commit()
    return updated_menu.scalar()


async def delete_menu_by_id(id: uuid.UUID, session: AsyncSession) -> MenuSchema | None:
    deleted_menu: AsyncResult = await session.execute(sa.delete(Menu).returning(Menu).where(Menu.id == id))
    await session.commit()
    return deleted_menu.scalar()


async def count_submenu(menu_id: uuid.UUID, session: AsyncSession) -> int:
    result = await session.execute(
        sa.select(func.count(Submenu.id)).join(Menu.submenu).where(Menu.id == menu_id))
    return result.scalar()


async def count_dishes(menu_id: uuid.UUID, session: AsyncSession) -> int:
    result = await session.execute(
        sa.select(func.count(Dish.id))
        .join(Menu.submenu)
        .join(Submenu.dishes)
        .where(Menu.id == menu_id))
    return result.scalar()
