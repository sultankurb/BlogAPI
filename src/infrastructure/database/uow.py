from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class BaseUnitOfWork:
    def __init__(
            self,
            session_maker: async_sessionmaker[AsyncSession]
    ) -> None:
        self.session_maker = session_maker
        self.session: AsyncSession | None = None

    async def __aenter__(self):
        self.session = self.session_maker()
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
