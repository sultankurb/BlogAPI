from src.config.exception import ApplicationException
from src.domain.identity.schemas.users import UsersCreateModel
from src.domain.identity.services.password_service import PasswordService
from src.infrastructure.database.uow import UnitOfWork


class UsersRegisterUseCase:
    def __init__(self, uow: UnitOfWork, password_service: PasswordService):
        self.uow = uow
        self.password_service = password_service

    async def execute(self, user: UsersCreateModel):
        async with self.uow as uow:
            existing_user = await uow.users.get_user_by_email(
                email=user.email
            )
            if existing_user:
                raise ApplicationException(message="Email already exists")
            hashed_pwd = self.password_service.hash_password(
                password=user.password
            )
            new_user = await uow.users.create_user(
                email=user.email,
                password_hash=hashed_pwd,
            )
            existing_profile = await uow.profiles.get_profile_by_username(
                username=user.username
            )
            if existing_profile:
                raise ApplicationException(message="Username already exists")
            await uow.profiles.create_profile(
                username=user.username,
                user_pk=new_user.pk,
            )
            await uow.commit()
            return new_user.pk
