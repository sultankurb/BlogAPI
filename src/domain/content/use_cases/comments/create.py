from src.domain.content.schemas.comments import CommentsCreate
from src.domain.content.use_cases.uow import ContentUow


class CommentsCreateUseCase:
    def __init__(self, uow: ContentUow):
        self._uow = uow

    async def execute(self, author_pk: int, new_comment: CommentsCreate):
        data = new_comment.model_dump()
        data['author_pk'] = author_pk
        async with self._uow as uow:
            new_comment_answer = await uow.comments.create_comment(
                data=data
            )
            await uow.commit()
            return new_comment_answer

