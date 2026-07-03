from src.config.exception import ApplicationException
from src.domain.identity.schemas.token import Token
from src.domain.identity.services.jwt_service import JWTService
from src.domain.identity.services.password_service import PasswordService
from src.domain.identity.use_cases.uow import IdentityUow


class LoginUseCase:
    def __init__(
        self,
        uow: IdentityUow,
        jwt_service: JWTService,
        password_service: PasswordService,
    ) -> None:
        self.uow = uow
        self._jwt_service = jwt_service
        self._password_service = password_service

    async def execute(self, email: str, password: str) -> Token:
        async with self.uow as uow:
            user = await uow.users.get_user_by_email_with_roles(email=email)
            if user is None:
                raise ApplicationException(message="Invalid email or password")
            if not self._password_service.verify_password(
                password=password, hashed_password=user.password
            ):
                raise ApplicationException(message="Invalid email or password")
            user_pk = user.pk
            roles = [role.name for role in user.roles]

        tokens = await self._jwt_service.create_user_session(
            user_pk=user_pk, roles=roles
        )
        return Token(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
        )
