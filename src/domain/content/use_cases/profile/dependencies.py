from src.domain.content.schemas import ProfileReadModel
from src.domain.content.use_cases.profile.create import CreateProfileUseCase
from src.domain.content.use_cases.profile.get import (
    ProfileGetByPKUseCase,
    ProfileGetByUsernameUseCase,
)
from src.domain.content.use_cases.uow import ContentUow
from src.infrastructure.database import session_factory


async def get_profile_by_pk_factory(pk: int) -> ProfileReadModel:
    use_case = ProfileGetByPKUseCase(uow=ContentUow(session_factory))
    profile = await use_case.execute(pk=pk)
    return profile


async def create_new_profile_factory(
        username: str,
        user_pk: int
) -> ProfileReadModel:
    user_case = CreateProfileUseCase(uow=ContentUow(session_factory))
    new_profile = await user_case.execute(username=username, user_pk=user_pk)
    return new_profile


async def get_profile_by_username_factory(username: str):
    use_case = ProfileGetByUsernameUseCase(uow=ContentUow(session_factory))
    profile = await use_case.execute(username=username)
    return profile