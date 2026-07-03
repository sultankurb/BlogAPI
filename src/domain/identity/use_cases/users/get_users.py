from src.config.exception import ForbiddenException
from src.domain.content.use_cases.profile.dependencies import (
    get_profile_by_pk_factory,
)
from src.domain.identity.schemas.users import (
    ProfileModel,
    UserReadModel,
    UserStatus,
)
from src.domain.identity.use_cases.uow import IdentityUow


class GetCurrentUserUseCase:
    def __init__(self, uow: IdentityUow) -> None:
        self._uow = uow

    async def execute(self, user_pk: int) -> UserReadModel:
        async with self._uow as uow:
            user = await uow.users.get_user_by_pk(pk=user_pk)
            if user.status != UserStatus.ACTIVE:
                raise ForbiddenException(
                    message="You are not verified user"
                )
            profile = await get_profile_by_pk_factory(pk=user_pk)
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
