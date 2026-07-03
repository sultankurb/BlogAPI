from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.content.schemas.posts import (
    PostsCreate,
    PostsFilters,
    PostsUpdate,
)
from src.infrastructure.database.base_repo import BaseRepository
from src.infrastructure.database.models import PostsORM


class PostsRepository(BaseRepository[PostsORM]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=PostsORM)

    async def get_post_by_pk(self, pk: int) -> PostsORM | None:
        post = await self._get_by_pk(pk=pk)
        return post

    async def get_posts(
            self,
            posts_filter: PostsFilters
    ) -> Sequence[PostsORM]:
        stmt = select(self._model_cls)

        if posts_filter.slug is not None:
            stmt.where(self._model_cls.slug == posts_filter.slug)

        if posts_filter.title is not None:
            stmt.where(self._model_cls.title == posts_filter.title)

        if posts_filter.author_pk is not None:
            stmt.where(self._model_cls.author_pk == posts_filter.author_pk)

        if posts_filter.last_seen_pk is not None:
            stmt.where(self._model_cls.pk < posts_filter.last_seen_pk)

        posts = await self._session.execute(stmt)

        return posts.scalars().all()

    async def create_new_post(
            self,
            post: PostsCreate,
            author_pk: int,
    ) -> PostsORM | None:
        post_orm = PostsORM(
            title=post.title,
            slug=post.slug,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
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
