from src.infrastructure.database import UnitOfWork


class SeedRolesUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, roles: list[str]) -> None:
        async with self.uow as uow:
            for role in roles:
                await uow.roles.create_if_not_exists(role)

            await uow.commit()
