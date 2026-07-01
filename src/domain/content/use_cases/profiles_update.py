from src.domain.content.schemas import ProfileReadModel, ProfileUpdatedModel
from src.infrastructure.database import UnitOfWork


class ProfilesUpdateUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(
        self, pk: int, data: ProfileUpdatedModel, partial: bool = False
    ) -> ProfileReadModel:
        data.model_dump(exclude_unset=partial)
        async with self._uow as uow:
            result = await uow.update_profile(pk=pk, data=data)

        return ProfileReadModel(
            first_name=result.first_name,
            last_name=result.last_name,
            biograph=result.biograph,
            username=result.username,
        )
