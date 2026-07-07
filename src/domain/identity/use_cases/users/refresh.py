from redis.asyncio import Redis

from src.config.exception import ForbiddenException
from src.domain.identity.schemas.token import Token
from src.domain.identity.services import JWTService
from src.domain.identity.use_cases.uow import IdentityUow


class RefreshJWTUseCase:
    def __init__(
            self,
            jwt_service: JWTService,
            redis: Redis,
            uow: IdentityUow
    ):
        self._jwt_service = jwt_service
        self._redis = redis
        self._uow = uow

    async def execute(self, refresh_toke: str) -> Token:
        query = f"refresh_token:{refresh_toke}"
        user_pk = await self._redis.get(query)
        if user_pk is None:
            raise ForbiddenException(
                message="There is no user with this refresh token"
            )
        async with self._uow as uow:
            user = await uow.users.get_by_pk_with_roles(pk=int(user_pk))
            if user is None:
                raise ForbiddenException(
                    message="User associated with this token no longer exists"
                )
            pk = user.pk
            roles = [role.name for role in user.roles]

        new_tokens = await self._jwt_service.create_user_session(
            user_pk=pk, roles=roles
        )
        await self._redis.delete(query)
        return Token.model_validate(new_tokens)
