from fastapi import Depends, FastAPI
from redis.asyncio.client import Redis

from python_code import db
from python_code.db import init_db
from python_code.redis import get_redis_connection

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


# todo логировать анвалидацию кеша
# TODO написать конструктор url адреса

@app.on_event('startup')
async def on_startup():
    await init_db(db.engine)


@app.get('/')
async def root(r: Redis = Depends(get_redis_connection)):
    await r.set(name='lol', value='kek')
    response = r.get('lol')
    return [{'message': 'Hello World', }, response]
