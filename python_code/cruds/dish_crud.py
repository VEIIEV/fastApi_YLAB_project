import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Session

from python_code.models.dish_model import Dish
from python_code.schemas.dish_schemas import DishSchema, CreateDish


def round_price(dish: Dish):
    "brings the price to  x.xx format"
    dish.price = format(dish.price, '.2f')


def get_dish_all(session: Session) -> [DishSchema]:
    result = session.execute(sa.select(Dish))
    return result.scalars().all()


def get_dish_for_submenu_all(submenu_id: uuid.UUID, session: Session):
    result = session.execute(sa.select(Dish).where(Dish.submenu_id == submenu_id))
    return result.scalars().all()


def get_dish_by_id(id: uuid.UUID, session: Session) -> DishSchema:
    result = session.execute(sa.select(Dish).where(Dish.id == id))
    return result.scalar()


def is_exist_dish(title: str, session: Session) -> bool:
    smtp = sa.select(Dish.id).join(Dish.submenu).where(Dish.title == title)
    checker = session.execute(smtp).scalar()
    if checker:
        return True
    else:
        return False


def create_dish(submenu_id: uuid.UUID, dish: CreateDish, session: Session) -> DishSchema:
    result = session.execute(sa.insert(Dish).returning(Dish),
                             [{'title': dish.title,
                               'description': dish.description,
                               'price': dish.price,
                               'submenu_id': submenu_id}])
    session.commit()
    return result.scalar()


def update_dish_by_id(submenu_id: uuid.UUID, dish_id: uuid.UUID, dish: CreateDish, session: Session):
    result = session.connection().execute(sa.update(Dish).where(Dish.id == dish_id).returning(Dish),
                                          [{'title': dish.title,
                                            'description': dish.description,
                                            'price': dish.price,
                                            'submenu_id': submenu_id}])
    session.commit()
    return result.scalar()


def delete_dish_by_id(id: uuid.UUID, session: Session) -> DishSchema:
    result = session.execute(sa.delete(Dish).returning(Dish).where(Dish.id == id))
    session.commit()
    return result.scalar()

# def create_dish(dish, se)
# нам нужно что бы блюдо не было ни в одном другом подменю
# то есть перед тем как его добавить нужно
# проверить нет ли его в других меню,
# if dish  not in
# (select dish.name from submenu join dish on id=dish.submenu_id)
