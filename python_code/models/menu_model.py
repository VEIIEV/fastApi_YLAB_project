import uuid
from typing import List

from sqlalchemy import String, Integer
from sqlalchemy import orm
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from python_code.db import Base
from python_code.models.submenu_model import Submenu


class Menu(Base):
    __tablename__ = 'menu'

    id: orm.Mapped[UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title: orm.Mapped[str] = orm.mapped_column(String)
    description: orm.Mapped[str] = orm.mapped_column(String)

    # пример подсчёта динамических данных налету
    # count: orm.Mapped[int] = orm.column_property(sa.select(
    #     sa.func.count(Submenu.id)).where(Submenu.menu_id == id).correlate_except(Submenu).as_scalar()
    #                                              )
    submenu: orm.Mapped[List["Submenu"]] = orm.relationship("Submenu", back_populates='menu')
