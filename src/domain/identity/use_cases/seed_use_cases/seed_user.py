import logging

from src.domain.content.use_cases.profile.dependencies import (
    create_new_profile_factory,
)
from src.domain.identity.schemas.roles import RolesEnum
from src.domain.identity.schemas.users import UserStatus
from src.domain.identity.services.password_service import PasswordService
from src.domain.identity.use_cases.uow import IdentityUow

logger = logging.getLogger(__name__)


class RootUserUseCase:
    def __init__(self, uow: IdentityUow, password_service: PasswordService):
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
            profile = await create_new_profile_factory(
                user_pk=admin.pk, username=username
            )
            logger.info(msg=f"{profile.username} created")
            await uow.commit()
