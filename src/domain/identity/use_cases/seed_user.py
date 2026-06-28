import logging

from src.domain.identity.dto import RolesEnum, UserStatus
from src.infrastructure.database import UnitOfWork

logger = logging.getLogger(__name__)


class SeedUserUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, email: str, password: str, username: str) -> None:
        try:
            async with self.uow as uow:
                admin = await uow.users.create_user(
                    email=email,
                    password=password,
                    role=RolesEnum.ADMIN.value,
                    status=UserStatus.ACTIVE
                )
                await uow.profiles.create_profile(
                    user_pk=admin.pk,
                    username=username
                )
                await uow.commit()
        except Exception as e:
            logger.error(e)