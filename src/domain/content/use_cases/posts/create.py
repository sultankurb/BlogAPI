import logging

from src.config.exception import ApplicationException
from src.domain.content.schemas.posts import PostsCreate, PostsRead
from src.domain.content.use_cases.uow import ContentUow

logger = logging.getLogger(__name__)

class PostCreateUseCase:
    def __init__(self, uow: ContentUow) -> None:
        self._uow = uow

    async def execute(self, data: PostsCreate, author_pk: int) -> PostsRead:
        async with self._uow as uow:
            try:
                new_post = await uow.posts.create_new_post(
                    post=data,
                    author_pk=author_pk
                )
                await uow.commit()
                return PostsRead.model_validate(obj=new_post)
            except Exception as e:
                logger.error(e)
                await uow.rollback()
                raise ApplicationException(message="Author not found")
