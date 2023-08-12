import uuid

from pydantic import BaseModel, Field

from python_code.schemas.dish_schemas import BaseDish, DishSchema


class BaseSubmenu(BaseModel):
    title: str = Field(title="dish's title", description='cant be null', max_length=200)
    description: str = Field(default='')


class CreateSubmenu(BaseSubmenu):
    pass


class SubmenuSchema(BaseSubmenu):
    id: uuid.UUID
    menu_id: uuid.UUID = Field(description='ref to his menu')
    dishes: list[BaseDish] = []

    class Config:
        from_attributes = True


class SubmenuExpandedSchema(BaseSubmenu):
    id: uuid.UUID
    menu_id: uuid.UUID = Field(description='ref to his menu')
    dishes: list[DishSchema] = []

    class Config:
        from_attributes = True
        exclude = {'id'}
