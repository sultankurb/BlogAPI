from src.domain.content.schemas.profile import ProfileReadModel
from src.domain.content.use_cases.uow import ContentUow


class ProfileGetByPKUseCase:
    def __init__(self, uow: ContentUow):
        self._ouw = uow

    async def execute(self, pk: int) -> ProfileReadModel | None:
        async with self._ouw as uow:
            profile = await uow.profiles.get_profile_by_pk(pk=pk)

        return ProfileReadModel.model_validate(obj=profile)


class ProfileGetByUsernameUseCase:
    def __init__(self, uow: ContentUow):
        self._ouw = uow

    async def execute(self, username: str) -> ProfileReadModel | None:
        async with self._ouw as uow:
            profile = await uow.profiles.get_profile_by_username(username=username)
        if profile is None:
            return None

        return ProfileReadModel.model_validate(obj=profile)
