from src.config.exception import ForbiddenException, NotFoundException
from src.domain.content.schemas.comments import CommentsUpdate
from src.domain.content.use_cases.uow import ContentUow


class CommentsUpdateUsaCase:
    def __init__(self, uow: ContentUow):
        self._uow = uow

    async def execute(self, pk: int, user: dict, to_update: CommentsUpdate):
        async with self._uow as uow:
            check = await uow.comments.get_by_pk(pk=pk)
            if check is None:
                raise NotFoundException(message="Comment not found")
            if check.author_pk == int(user["sub"]) or "admin" in user["roles"]:
                result = await uow.comments.update_comment(
                    pk=pk, data=to_update.model_dump()
                )
                await uow.commit()
                return result
            raise ForbiddenException(
                message="You are not allowed to delete this comment"
            )
