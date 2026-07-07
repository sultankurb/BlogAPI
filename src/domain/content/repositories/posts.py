from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.domain.content.schemas.posts import (
    PostsCreate,
    PostsFilters,
    PostsUpdate,
)
from src.infrastructure.database.base_repo import BaseRepository
from src.infrastructure.database.models import CommentsORM, PostsORM


class PostsRepository(BaseRepository[PostsORM]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=PostsORM)

    async def get_post_by_pk(self, pk: int) -> PostsORM | None:
        stmt = select(self._model_cls).where(self._model_cls.pk == pk).options(
            joinedload(self._model_cls.comments).joinedload(CommentsORM.author)
        ).options(joinedload(self._model_cls.author))
        result = await self._session.execute(stmt)
        return result.scalars().unique().first()

    async def get_posts(
            self,
            posts_filter: PostsFilters
    ) -> Sequence[PostsORM]:
        stmt = (
            select(self._model_cls)
            .options(joinedload(self._model_cls.author))
        )

        if posts_filter.slug is not None:
            stmt = stmt.where(self._model_cls.slug == posts_filter.slug)

        if posts_filter.title is not None:
            stmt = stmt.where(self._model_cls.title == posts_filter.title)

        if posts_filter.author_pk is not None:
            stmt = stmt.where(
                self._model_cls.author_pk == posts_filter.author_pk
            )

        if posts_filter.last_seen_pk is not None:
            stmt = stmt.where(self._model_cls.pk > posts_filter.last_seen_pk)

        stmt = stmt.order_by(self._model_cls.pk.asc())

        stmt = stmt.limit(posts_filter.limit)

        result = await self._session.execute(stmt)

        return result.scalars().all()


    async def create_new_post(
            self,
            post: PostsCreate,
            author_pk: int,
    ) -> PostsORM | None:
        post_orm = PostsORM(
            title=post.title,
            slug=post.slug,
            content=post.content,
            author_pk=author_pk,
        )
        result = await self._add(obj=post_orm)
        return result

    async def delete_post(self, pk: int) -> bool:
        result = await self._delete_by_pk(pk=pk)
        return result

    async def update_post(
            self,
            pk: int,
            post: PostsUpdate,
    ) -> PostsORM | None:
        result = await self._update(
            pk=pk,
            data=post.model_dump(exclude_unset=True)
        )
        return result
