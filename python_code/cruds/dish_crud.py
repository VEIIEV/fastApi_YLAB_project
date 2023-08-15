import uuid
from typing import Sequence

import sqlalchemy as sa
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession

from python_code.models.dish_model import Dish
from python_code.schemas.dish_schemas import CreateDish, DishSchema, CreateDishWithId


async def get_dish_all(session: AsyncSession) -> list[DishSchema]:
    result: AsyncResult = await session.execute(sa.select(Dish))
    return result.scalars().all()


async def get_dish_for_submenu_all(submenu_id: uuid.UUID, session: AsyncSession) -> Sequence[DishSchema]:
    result: AsyncResult = await session.execute(sa.select(Dish).where(Dish.submenu_id == submenu_id))
    return result.scalars().all()


async def get_dish_by_id(id: uuid.UUID, session: AsyncSession) -> DishSchema | None:
    result = await session.execute(sa.select(Dish).filter_by(id=id))
    return result.scalar()


async def is_exist_dish(title: str, session: AsyncSession) -> bool:
    smtp: Select = sa.select(Dish.id).join(Dish.submenu).where(Dish.title == title)
    checker = await session.execute(smtp)
    if checker:
        return True
    else:
        return False


async def create_dish(submenu_id: uuid.UUID, dish: CreateDish | CreateDishWithId,
                      session: AsyncSession) -> DishSchema | None:
    data = dish.model_dump(exclude_unset=True)
    result: AsyncResult = await session.execute(sa.insert(Dish).returning(Dish).values(**data))
    await session.commit()
    return result.scalar()


# todo чёт тут какая-то ёбань
async def update_dish_by_id(submenu_id: uuid.UUID, dish_id: uuid.UUID, dish: CreateDish,
                            session: AsyncSession):
    data = dish.model_dump(exclude_unset=True)

    result = await session.execute(sa.update(Dish).where(Dish.id == dish_id).returning(Dish).
                                   values(**data))
    await session.commit()
    return result.scalar()


async def delete_dish_by_id(id: uuid.UUID, session: AsyncSession) -> DishSchema | None:
    result: AsyncResult = await session.execute(sa.delete(Dish).returning(Dish).where(Dish.id == id))
    await session.commit()
    return result.scalar()

# def create_dish(dish, se)
# нам нужно что бы блюдо не было ни в одном другом подменю
# то есть перед тем как его добавить нужно
# проверить нет ли его в других меню,
# if dish  not in
# (select dish.name from submenu join dish on id=dish.submenu_id)
