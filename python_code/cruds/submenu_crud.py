import uuid
from typing import Sequence

import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession
from sqlalchemy.sql.expression import func

from python_code.models.dish_model import Dish
from python_code.models.submenu_model import Submenu
from python_code.schemas.submenu_schemas import CreateSubmenu, SubmenuSchema


async def get_submenu_all(session: AsyncSession) -> Sequence[SubmenuSchema]:
    result: AsyncResult = await session.execute(sa.select(SubmenuSchema))
    return result.scalars().all()


async def get_submenu_by_id(id: uuid.UUID, session: AsyncSession) -> SubmenuSchema | None:
    query = select(Submenu).filter(Submenu.id == id)
    result = await session.execute(query)
    # result = await session.execute(select(text('submenu')).where(Submenu.id == id))
    #  query = select(UserQuestionnaire).order_by(UserQuestionnaire.city).fetch(10)
    #     result = await session.execute(query)
    #     return result.scalars().fetchall()
    return result.scalar()


async def create_submenu(menu_id: uuid.UUID, submenu: CreateSubmenu, session: AsyncSession) -> SubmenuSchema | None:
    created_submenu = await session.execute(sa.insert(Submenu).returning(Submenu),
                                            [{'title': submenu.title,
                                              'description': submenu.description,
                                              'menu_id': menu_id}])
    await session.commit()
    return created_submenu.scalar()


# todo переделать update (наверное)
async def update_submenu_by_id(menu_id: uuid.UUID, submenu_id: uuid.UUID, submenu: CreateSubmenu,
                               session: AsyncSession) -> uuid.UUID | None:
    updated_submenu = await session.execute(
        sa.update(Submenu).where(Submenu.id == submenu_id).returning(Submenu).values(
            title=submenu.title,
            description=submenu.description,
            menu_id=menu_id))
    await session.commit()
    return updated_submenu.scalar()


async def delete_submenu_by_id(id: uuid.UUID, session: AsyncSession) -> SubmenuSchema | None:
    deleted_submenu: AsyncResult = await session.execute(sa.delete(Submenu).returning(Submenu).where(Submenu.id == id))
    await session.commit()
    return deleted_submenu.scalar()


async def count_dishes(submenu_id: uuid.UUID, session: AsyncSession) -> int:
    result: AsyncResult = await session.execute(
        sa.select(func.count(Dish.id))
        .join(Submenu.dishes)
        .where(Submenu.id == submenu_id))
    return result.scalar()
