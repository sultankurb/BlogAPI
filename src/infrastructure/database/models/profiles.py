from sqlalchemy import BigInteger, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import BaseORM


class ProfilesORM(BaseORM):
    __tablename__ = "profiles"
    user_pk: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(column="users.pk", ondelete="CASCADE"),
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(Text(), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(Text(), nullable=True)
    last_name: Mapped[str] = mapped_column(Text(), nullable=True)
    biography: Mapped[str] = mapped_column(Text(), nullable=True)
