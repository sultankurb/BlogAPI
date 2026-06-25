from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base import BaseORM

if TYPE_CHECKING:
    from src.infrastructure.database.models.users import UsersORM


class RolesORM(BaseORM):
    __tablename__ = "roles"
    pk: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    users: Mapped[List[UsersORM]] = relationship(
        "UsersORM",
        secondary="users_roles",
        back_populates="roles",
    )
