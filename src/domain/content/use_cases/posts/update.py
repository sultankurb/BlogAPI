from src.config.exception import ForbiddenException, NotFoundException
from src.domain.content.schemas.posts import PostsUpdate
from src.domain.content.use_cases.uow import ContentUow


class PostUpdateUseCase:
    def __init__(self, uow: ContentUow) -> None:
        self._uow = uow

    async def execute(self, post_pk: int, user: dict, data: PostsUpdate):
        async with self._uow as uow:
            post = await uow.posts.get_post_by_pk(pk=post_pk)
            if post is None:
                raise NotFoundException(message="Post not found")
            if post.author_pk == int(user["sub"]) or "admin" in user["roles"]:
                result = await uow.posts.update_post(
                    pk=post.pk,
                    post=data
                )
                await uow.commit()
                return result
            raise ForbiddenException(
                message="You are not allowed to update this post"
            )
