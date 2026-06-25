from src.config.exception import ApplicationException
from src.domain.identity.schemas.token import Token
from src.domain.identity.services.jwt_service import JWTService
from src.domain.identity.services.password_service import PasswordService
from src.infrastructure.database import UnitOfWork


class LoginUseCase:
    def __init__(
            self,
            uow: UnitOfWork,
            jwt_service: JWTService = JWTService(),
            password_service: PasswordService = PasswordService(),
    ) -> None:
        self.uow = uow
        self._jwt_service = jwt_service
        self._password_service = password_service

    async def execute(self, email: str, password: str) -> Token :
        async with self.uow as uow:
            user = await uow.users.get_user_by_email_with_roles(email=email)
            if user is None:
                raise ApplicationException(
                    message="Error there is no user with this email, check your email"
                )
            if not self._password_service.verify_password(
                    password=password,
                    hashed_password=user.password
            ):
                raise ApplicationException(message="Password is incorrect")
            tokens = await self._jwt_service.create_user_session(
                user_pk=user.pk,
                roles=user.roles
            )
            return Token(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
            )

