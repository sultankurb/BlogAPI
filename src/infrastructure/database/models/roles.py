from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import BaseORM


class RolesORM(BaseORM):
    __tablename__ = "roles"
    pk: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(Text(), nullable=False)
