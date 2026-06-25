from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.identity.dto import UserStatus
from src.infrastructure.database.models.base import BaseORM

if TYPE_CHECKING:
    from src.infrastructure.database.models.roles import RolesORM

class UsersORM(BaseORM):
    __tablename__ = "users"
    pk: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    email: Mapped[str] = mapped_column(Text())
    password: Mapped[str] = mapped_column(Text())
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, native_enum=True),
        default=UserStatus.PENDING,
        nullable=False,
    )
    roles: Mapped[List[RolesORM]] = relationship(
        "RolesORM",
        secondary="users_roles",
        back_populates="users"
    )
