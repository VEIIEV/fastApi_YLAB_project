import uuid
from typing import List

from pydantic import BaseModel, Field

from python_code.schemas.submenu_schemas import BaseSubmenu


class BaseMenu(BaseModel):
    title: str = Field(title="dish's title", description='cant be null', max_length=200)
    description: str = Field(default='')


class CreateMenu(BaseMenu):
    pass


class MenuSchema(BaseMenu):
    id: uuid.UUID
    submenu: List[BaseSubmenu] | None = None


    class Config:
        from_attributes = True
