from src.config.exception import ForbiddenException, NotFoundException
from src.domain.content.use_cases.uow import ContentUow


class CommentsDeleteUsaCase:
    def __init__(self, uow: ContentUow):
        self._uow = uow
    
    async def execute(self, pk: int, user: dict) -> None:
        async with self._uow as uow:
            check = await uow.comments.get_by_pk(pk=pk)
            if check is None:
                raise NotFoundException(message="Comment not found")
            if check.author_pk == int(user["sub"]) or "admin" in user["roles"]:
                await uow.comments.delete_comment(pk=pk)
                await uow.commit()
                return
            raise ForbiddenException(
                message="You are not allowed to delete this comment"
            )