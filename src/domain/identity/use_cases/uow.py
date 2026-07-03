from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.identity.repositories.roles import RolesRepository
from src.domain.identity.repositories.users import UsersRepository
from src.infrastructure.database.uow import BaseUnitOfWork


class IdentityUow(BaseUnitOfWork):
    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_maker=session)
        self._users: UsersRepository | None = None
        self._roles: RolesRepository | None = None

    @property
    def users(self) -> UsersRepository:
        if self._users is None:
            self._users = UsersRepository(self.session)
        return self._users

    @property
    def roles(self) -> RolesRepository:
        if self._roles is None:
            self._roles = RolesRepository(self.session)
        return self._roles
