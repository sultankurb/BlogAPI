import src.config.exception
from src.domain.identity.dto import UserStatus
from src.domain.identity.schemas.users import ProfileModel, UserReadModel
from src.infrastructure.database import UnitOfWork


class GetCurrentUserUseCase:
    def __init__(self, ouw: UnitOfWork):
        self._ouw = ouw

    async def execute(self,user_pk: int) -> UserReadModel:
        async with self._ouw as uow:
            user = await uow.users.get_user_by_pk(
                pk=user_pk
            )
            if user.status != UserStatus.ACTIVE:
                raise src.config.exception.ForbiddenException(
                    message="You are not verified user"
                )
            profile = await uow.profiles.get_profile_by_pk(
                pk=user_pk
            )
            return UserReadModel(
                email=user.email,
                status=user.status,
                profile=ProfileModel(
                    user_pk=profile.user_pk,
                    biography=profile.biography,
                    first_name=profile.first_name,
                    last_name=profile.last_name,
                    username=profile.username,
                ),
            )
