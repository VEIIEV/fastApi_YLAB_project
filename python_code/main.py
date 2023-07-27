from typing import Annotated

from fastapi import Depends, Path, HTTPException, FastAPI
from sqlalchemy.orm import Session

import python_code.cruds.menu_crud
from python_code import db
from python_code.cruds import dish_crud as DC
from python_code.routers import menu_router, submenu_router, dish_router
from python_code.db import init_db, get_session

# что бы meta_create_all отработал нужно импортировать классы таблиц, мерзость
from python_code.models.dish_model import Dish
from python_code.models.menu_model import Menu
from python_code.models.submenu_model import Submenu

#################################################################################
app = FastAPI()
app.include_router(menu_router.router)
app.include_router(submenu_router.router)
app.include_router(dish_router.router)


@app.on_event("startup")
async def on_startup():
    init_db(db.engine)


# TODO убрать тестовые пути
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping/{value}")
def ping(value: str):
    return {"value": value}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/check/dish/{title}")
def check_dish_existence(title: Annotated[str, Path(title="The ID of the item to get")],
                         session: Session = Depends(get_session)):
    return DC.is_exist_dish(title, session)


@app.get("/check")
def delete_later(session: Session = Depends(get_session)):
    menus = python_code.cruds.menu_crud.get_menu_all(session)
    for elem in menus:
        elem[0] = 'dicpic'
    return menus
# пути к меню


# endpoint for submenu
