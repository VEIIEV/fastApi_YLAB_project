import uuid
from decimal import Decimal, getcontext

from pydantic import BaseModel, Field



class BaseDish(BaseModel):
    title: str = Field(title="dish's title", description='cant by null', max_length=200)
    description: str = Field(default='')
    price: Decimal = Field(title="dish's price", description="decimal, must be gt then 0", gt=0)


class CreateDish(BaseDish):
    pass


class DishSchema(BaseDish):
    id: uuid.UUID
    submenu_id: uuid.UUID = Field(description="ref to his submenu")

    class Config:
        from_attributes = True
