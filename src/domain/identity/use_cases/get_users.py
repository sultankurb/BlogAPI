import logging

from src.config.exception import ApplicationException, ForbiddenException
from src.domain.identity.schemas.users import ProfileModel, UserReadModel
from src.domain.identity.services.jwt_service import JWTService
from src.infrastructure.database import UnitOfWork


class GetCurrentUserUseCase:
    def __init__(self, ouw: UnitOfWork, jwt_service: JWTService):
        self._ouw = ouw
        self._jwt_service = jwt_service

    async def execute(self, token: str) -> UserReadModel:
        decoded_token = self._jwt_service.decode_token(token=token)
        async with self._ouw as uow:
            user = await uow.users.get_user_by_pk(pk=int(decoded_token["sub"]))
            if not user:
                raise ForbiddenException(message="Token is invalid")
            profile = await uow.profiles.get_profile_by_pk(
                pk=int(decoded_token["sub"])
            )
            return UserReadModel(
                email=user.email,
                profile=ProfileModel(
                    user_pk=profile.user_pk,
                    biography=profile.biography,
                    first_name=profile.first_name,
                    last_name=profile.last_name,
                    username=profile.username,
                )
            )
