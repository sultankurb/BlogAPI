import logging

from sqlalchemy.exc import IntegrityError, NoForeignKeysError

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
                return PostsRead(
                    pk=new_post.pk,
                    slug=new_post.slug,
                    title=new_post.title,
                    content=new_post.content,
                    created_at=new_post.created_at,
                    updated_at=new_post.updated_at,
                    author_pk=new_post.author_pk,
                    author=None

                )
            except IntegrityError as e:
                logger.error(e)
                await uow.rollback()
                raise ApplicationException(message="Slug already exists")

            except NoForeignKeysError as e:
                logger.error(e)
                await uow.rollback()
                raise ApplicationException(
                    message="Failed to create new post check your profile"
                )
