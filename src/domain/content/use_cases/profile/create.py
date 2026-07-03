from src.domain.content.schemas import ProfileReadModel
from src.domain.content.use_cases.uow import ContentUow


class CreateProfileUseCase:
    def __init__(self, uow: ContentUow):
        self._uow = uow

    async def execute(self, username: str, user_pk: int) -> ProfileReadModel:
        async with self._uow as uow:
            new_profile = await uow.profiles.create_profile(
                username=username,
                user_pk=user_pk
            )
            await uow.commit()

        return ProfileReadModel.model_validate(obj=new_profile)
