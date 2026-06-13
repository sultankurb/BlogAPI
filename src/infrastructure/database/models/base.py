from datetime import datetime

from sqlalchemy import BigInteger, DateTime, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseORM(DeclarativeBase):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("TIMEZONE('utc', now())")
    )
