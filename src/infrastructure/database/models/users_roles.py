from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import BaseORM


class UserRoleORM(BaseORM):
    __tablename__ = "user_roles"
    __table_args__ = (
        UniqueConstraint(
            'user_pk',
            'role_pk',
            name='user_roles_pk_idx'
        ),
    )
    user_pk: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(
            column="users.pk",
            onupdate="CASCADE",
        )
    )
    role_pk: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(
            column="roles.pk",
            onupdate="CASCADE",
        )
    )
