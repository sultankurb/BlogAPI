from src.config.exception import ApplicationException, ForbiddenException
from src.domain.content.use_cases.uow import ContentUow


class PostDeleteUseCase:
    def __init__(self, uow: ContentUow) -> None:
        self._uow = uow

    async def execute(self, post_pk: int, user: dict):
        async with self._uow as uow:
            post = await uow.posts.get_post_by_pk(pk=post_pk)
            if post.author_pk == int(user["sub"]) or "admin" in user["roles"]:
                check = await uow.posts.delete_post(pk=post_pk)
                if not check:
                    raise ApplicationException(message="Post was not deleted")
                await uow.commit()
                return {"message": "Deleted successfully"}

            raise ForbiddenException(
                message="You are not allowed to delete this post"
            )