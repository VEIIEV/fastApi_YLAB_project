import decimal
import uuid

import sqlalchemy as sa
from sqlalchemy import String, DECIMAL
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID

from python_code.db import Base


class Dish(Base):
    __tablename__ = 'dishes'

    id: orm.Mapped[UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title: orm.Mapped[str] = orm.mapped_column(String)
    description: orm.Mapped[str] = orm.mapped_column(String)
    price: orm.Mapped[decimal.Decimal] = orm.mapped_column(DECIMAL(10, 2, decimal_return_scale=2))
    submenu_id: orm.Mapped[int] = orm.mapped_column(UUID(as_uuid=True), sa.ForeignKey('submenu.id', ondelete='CASCADE'))

    submenu: orm.Mapped["Submenu"] = orm.relationship("Submenu", back_populates='dishes')
