from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import BaseORM


class CommentsORM(BaseORM):
    __tablename__ = "comments"
    pk: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    author_pk: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            column="profiles.user_pk", onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    posts_pk: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(column="posts.pk", onupdate="CASCADE", ondelete="CASCADE"),
    )
