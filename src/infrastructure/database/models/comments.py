from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base import BaseORM

if TYPE_CHECKING:
    from src.infrastructure.database.models.posts import PostsORM
    from src.infrastructure.database.models.profiles import ProfilesORM

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
    post: Mapped[PostsORM] = relationship(
        "PostsORM",
        back_populates="comments",
    )
    author: Mapped[ProfilesORM] = relationship(
        "ProfilesORM",
        back_populates="comments",
    )
