from src.domain.content.schemas.posts import PostsCreate, PostsRead
from src.infrastructure.database import UnitOfWork


class PostCreateUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: PostsCreate, author_pk: int) -> PostsRead:
        async with self._uow as uow:
            new_post = await uow.posts.create_new_post(
                post=data,
                author_pk=author_pk
            )
            await uow.commit()
            return PostsRead.model_validate(obj=new_post)
