from typing import List

from src.config.exception import NotFoundException
from src.domain.content.schemas.posts import PostsFilters, PostsRead
from src.domain.content.use_cases.uow import ContentUow


class ReadPostsUseCase:
    def __init__(self, uow: ContentUow) -> None:
        self._uow = uow

    async def execute(
            self,
            posts_filters: PostsFilters,
    ) -> List[PostsRead | None]:
        async with self._uow as uow:
            posts = await uow.posts.get_posts(
                posts_filter=posts_filters
            )
            return [
                PostsRead.model_validate(
                    obj=post, from_attributes=True
                ) for post in posts
            ]

class ReadOnePostUseCase:
    def __init__(self, uow: ContentUow) -> None:
        self._uow = uow

    async def execute(self, pk: int):
        async with self._uow as uow:
            post = await uow.posts.get_post_by_pk(pk=pk)
            if post is None:
                raise NotFoundException(message="Post not found")
            return PostsRead.model_validate(obj=post, from_attributes=True)
