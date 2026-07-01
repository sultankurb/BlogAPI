from typing import Annotated

from fastapi import Depends

from src.domain.content.use_cases import ProfilesUpdateUseCase
from src.presentation.api.dependecies import UoWDep


def get_profile_update(uow: UoWDep) -> ProfilesUpdateUseCase:
    return ProfilesUpdateUseCase(uow=uow)


ProfileUpdateDepends = Annotated[
    ProfilesUpdateUseCase, Depends(get_profile_update)
]
