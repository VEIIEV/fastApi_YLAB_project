import uuid
from typing import List

import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID

from python_code.db import Base


class Submenu(Base):
    __tablename__ = 'submenu'

    id: orm.Mapped[UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title: orm.Mapped[str] = orm.mapped_column(String, unique=True)
    description: orm.Mapped[str] = orm.mapped_column(String)
    menu_id: orm.Mapped[UUID] = orm.mapped_column(UUID(as_uuid=True), sa.ForeignKey("menu.id", ondelete='CASCADE'))

    # relationship contain values from other tables related to this one
    dishes: orm.Mapped[List["Dish"]] = orm.relationship("Dish", back_populates='submenu')
    menu: orm.Mapped["Menu"] = orm.relationship("Menu", back_populates='submenu')
