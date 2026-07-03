from src.domain.content.schemas import ProfileReadModel, ProfileUpdatedModel
from src.domain.content.use_cases.uow import ContentUow


class ProfilesUpdateUseCase:
    def __init__(self, uow: ContentUow) -> None:
        self._uow = uow

    async def execute(
        self, pk: int, data: ProfileUpdatedModel, partial: bool = True
    ) -> ProfileReadModel:
        data.model_dump(exclude_unset=partial)
        async with self._uow as uow:
            result = await uow.profiles.update_profile(pk=pk, data=data)
            uow.commit()

        return ProfileReadModel(
            first_name=result.first_name,
            last_name=result.last_name,
            biograph=result.biograph,
            username=result.username,
        )
