from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base import BaseORM

if TYPE_CHECKING:
    from src.infrastructure.database.models.comments import CommentsORM
    from src.infrastructure.database.models.profiles import ProfilesORM


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
    author: Mapped["ProfilesORM"] = relationship(
        argument="ProfilesORM",
        back_populates="posts",
        primaryjoin="ProfilesORM.user_pk == PostsORM.author_pk",
    )
    comments: Mapped[List[CommentsORM]] = relationship(
        "CommentsORM",
        back_populates="post",
    )
