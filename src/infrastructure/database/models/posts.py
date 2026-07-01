from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import BaseORM


class PostsORM(BaseORM):
    __tablename__ = "posts"
    pk: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, unique=True)
    content: Mapped[str] = mapped_column(String)
    author_pk: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            column="profiles.user_pk", onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
