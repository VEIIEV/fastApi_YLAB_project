from fastapi import FastAPI

from python_code import db
from python_code.db import init_db

# что бы meta_create_all отработал нужно импортировать классы таблиц, мерзость
# from python_code.models.dish_model import Dish
# from python_code.models.menu_model import Menu
# from python_code.models.submenu_model import Submenu
from python_code.routers import dish_router, menu_router, submenu_router

#################################################################################
app = FastAPI()
app.include_router(menu_router.router)
app.include_router(submenu_router.router)
app.include_router(dish_router.router)


@app.on_event('startup')
async def on_startup():
    init_db(db.engine)


# TODO pickle dumps pickle.loads
@app.get('/')
async def root():
    return {'message': 'Hello World'}
