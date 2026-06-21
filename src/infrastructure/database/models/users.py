from sqlalchemy import BigInteger, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.identity.dto import UserStatus
from src.infrastructure.database.models.base import BaseORM


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
