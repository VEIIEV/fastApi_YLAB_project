from sqlalchemy.ext.asyncio import AsyncSession

from python_code.cruds import menu_crud as MC
from python_code.cruds import submenu_crud as SC
from python_code.schemas.dish_schemas import BaseDish, DishSchema


def round_price(dish: DishSchema | BaseDish | None) -> None:
    'brings the price to  x.xx format'
    if dish:
        dish.price = format(dish.price, '.2f')


async def add_dish_number_to_submenu(submenu, session: AsyncSession) -> None:
    'add dish_count to submenu'
    dishes_count = await SC.count_dishes(submenu.id, session)
    session.__setattr__('dishes_count', dishes_count)


async def add_counters_to_response(menu, session: AsyncSession) -> None:
    'Util func that add counter of dish and sub to menu resp'

    submenus_count = await MC.count_submenu(menu.id, session)
    dishes_count = await MC.count_dishes(menu.id, session)
    menu.__setattr__('submenus_count', submenus_count)
    menu.__setattr__('dishes_count', dishes_count)
