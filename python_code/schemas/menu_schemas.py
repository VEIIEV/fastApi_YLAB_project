import uuid

from pydantic import BaseModel, Field

from python_code.schemas.submenu_schemas import BaseSubmenu, SubmenuExpandedSchema


class BaseMenu(BaseModel):
    title: str = Field(title="dish's title", description='cant be null', max_length=200)
    description: str = Field(default='')


class CreateMenu(BaseMenu):
    pass


class CreateMenuWithId(BaseMenu):
    id: uuid.UUID


class MenuSchema(BaseMenu):
    id: uuid.UUID
    submenu: list[BaseSubmenu] = []

    class Config:
        from_attributes = True


class MenuExpandedSchema(BaseMenu):
    submenu: list[SubmenuExpandedSchema] = []

    class Config:
        from_attributes = True
        exclude = {'id'}
