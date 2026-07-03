from src.domain.identity.use_cases.uow import IdentityUow


class SeedRolesUseCase:
    def __init__(self, uow: IdentityUow) -> None:
        self.uow = uow

    async def execute(self, roles: list[str]) -> None:
        async with self.uow as uow:
            for role in roles:
                await uow.roles.create_if_not_exists(role)

            await uow.commit()
