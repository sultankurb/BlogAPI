from config.exception import ApplicationException, ForbiddenException
from src.infrastructure.database import UnitOfWork


class PostDeleteUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, post_pk: int, user_pk: int):
        async with self._uow as uow:
            post = await uow.posts.get_post_by_pk(pk=post_pk)
            if post.author_pk != user_pk:
                raise ForbiddenException(
                    message="You are not allowed to delete this post"
                )
            check = await uow.posts.delete_post(pk=post_pk)
            if not check:
                raise ApplicationException(message="Post was not deleted")
            return {"message": "Deleted successfully"}
