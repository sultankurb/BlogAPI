import logging

from fastapi import BackgroundTasks
from sqlalchemy.exc import IntegrityError

from src.config.exception import ApplicationException
from src.domain.content.use_cases.profile.dependencies import (
    create_new_profile_factory,
    get_profile_by_username_factory,
)
from src.domain.identity.schemas.users import (
    ProfileModel,
    UserReadModel,
    UsersCreateModel,
)
from src.domain.identity.services.password_service import PasswordService
from src.domain.identity.services.verification_service import (
    VerificationService,
)
from src.domain.identity.use_cases.uow import IdentityUow

logger = logging.getLogger(__name__)


class RegisterUseCase:
    def __init__(
        self,
        uow: IdentityUow,
        password_service: PasswordService,
        verification_service: VerificationService,
    ):
        self._uow = uow
        self._password_service = password_service
        self._verification_service = verification_service

    async def execute(
        self, user: UsersCreateModel, background_tasks: BackgroundTasks
    ) -> UserReadModel:
        hashed_pwd = self._password_service.hash_password(
            password=user.password
        )
        try:
            async with self._uow as uow:
                if await uow.users.get_user_by_email(email=user.email):
                    raise ApplicationException(message="Email already exists")
                if await get_profile_by_username_factory(
                    username=user.username
                ):
                    raise ApplicationException(
                        message="Username already exists"
                    )
                new_user = await uow.users.create_user(
                    email=user.email,
                    password_hash=hashed_pwd,
                )
                await uow.commit()
            try:
                new_profile = await create_new_profile_factory(
                    username=user.username, user_pk=new_user.pk
                )
            except Exception as e:
                logger.error(e)
                async with self._uow as uow:
                    await uow.users.delete_user_by_pk(pk=new_user.pk)
                    await uow.commit()

                raise ApplicationException(message="User creation failed")

            await self._verification_service.verification_code(
                email=new_user.email, background_tasks=background_tasks
            )

            return UserReadModel(
                email=new_user.email,
                status=new_user.status,
                profile=ProfileModel(
                    username=new_profile.username,
                    biography=new_profile.biography,
                    first_name=new_profile.first_name,
                    last_name=new_profile.last_name,
                    user_pk=new_user.pk,
                ),
            )
        except IntegrityError as e:
            logger.error(e)
            raise ApplicationException(
                message="Registration failed."
                " Email or Username is already taken"
            )
