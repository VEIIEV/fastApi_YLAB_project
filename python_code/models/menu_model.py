import uuid
from typing import List

from sqlalchemy import String, Integer
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID
from python_code.db import Base


class Menu(Base):
    __tablename__ = 'menu'

    id: orm.Mapped[UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title: orm.Mapped[str] = orm.mapped_column(String)
    description: orm.Mapped[str] = orm.mapped_column(String)

    submenu: orm.Mapped[List["Submenu"]] = orm.relationship("Submenu", back_populates='menu')
