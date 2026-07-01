import logging

from src.domain.identity.dto import RolesEnum, UserStatus
from src.domain.identity.services.password_service import PasswordService
from src.infrastructure.database import UnitOfWork

logger = logging.getLogger(__name__)


class RootUserUseCase:
    def __init__(self, uow: UnitOfWork, password_service: PasswordService):
        self._uow = uow
        self.__password_service = password_service

    async def execute(self, email: str, password: str, username: str) -> None:
        async with self._uow as uow:
            check = await uow.users.get_user_by_email(email=email)
            if check is not None:
                return

            admin = await uow.users.create_user(
                email=email,
                password_hash=self.__password_service.hash_password(password),
                role=RolesEnum.ADMIN.value,
                status=UserStatus.ACTIVE,
            )
            await uow.profiles.create_profile(
                user_pk=admin.pk, username=username
            )
            await uow.commit()
