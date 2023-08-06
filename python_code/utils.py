from python_code.cruds import menu_crud as MC
from python_code.cruds import submenu_crud as SC
from python_code.schemas.dish_schemas import DishSchema


def round_price(dish: DishSchema) -> None:
    'brings the price to  x.xx format'
    dish.price = format(dish.price, '.2f')


def add_dish_number_to_submenu(session, submenu) -> None:
    'add dish_count to submenu'
    dishes_count = SC.count_dishes(submenu.id, session)
    submenu.__setattr__('dishes_count', dishes_count)


def add_counters_to_response(menu, session) -> None:
    'Util func that add counter of dish and sub to menu resp'

    submenus_count = MC.count_submenu(menu.id, session)
    dishes_count = MC.count_dishes(menu.id, session)
    menu.__setattr__('submenus_count', submenus_count)
    menu.__setattr__('dishes_count', dishes_count)
