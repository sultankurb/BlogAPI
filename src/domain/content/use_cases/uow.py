from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.content.repositories.posts import PostsRepository
from src.domain.content.repositories.profile import ProfileRepository
from src.infrastructure.database.uow import BaseUnitOfWork


class ContentUow(BaseUnitOfWork):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        super().__init__(session_maker=session)
        self._profiles: ProfileRepository | None = None
        self._posts: PostsRepository | None = None

    @property
    def profiles(self) -> ProfileRepository:
        if self._profiles is None:
            self._profiles = ProfileRepository(self.session)
        return self._profiles

    @property
    def posts(self) -> PostsRepository:
        if self._posts is None:
            self._posts = PostsRepository(self.session)
        return self._posts
