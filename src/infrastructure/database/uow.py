from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.content.repositories.profile import ProfileRepository
from src.domain.identity.repositories.roles import RolesRepository
from src.domain.identity.repositories.users import UsersRepository
from src.infrastructure.database.connection import session_factory


class UnitOfWork:
    def __init__(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> None:
        self.session_maker = session_maker
        self.session: AsyncSession | None = None

        self._users: UsersRepository | None = None
        self._profiles: ProfileRepository | None = None
        self._roles: RolesRepository | None = None

    async def __aenter__(self):
        self.session = self.session_maker()
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    @property
    def users(self) -> UsersRepository:
        if self._users is None:
            self._users = UsersRepository(self.session)
        return self._users

    @property
    def profiles(self) -> ProfileRepository:
        if self._profiles is None:
            self._profiles = ProfileRepository(self.session)
        return self._profiles

    @property
    def roles(self) -> RolesRepository:
        if self._roles is None:
            self._roles = RolesRepository(self.session)
        return self._roles


def get_uow() -> UnitOfWork:
    return UnitOfWork(session_maker=session_factory)
