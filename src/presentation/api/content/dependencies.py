from typing import Annotated

from fastapi import Depends

from src.domain.content.use_cases import ProfilesUpdateUseCase
from src.domain.content.use_cases.uow import ContentUow
from src.infrastructure.database import session_factory


def get_content_uow():
    return ContentUow(session=session_factory)

ContentUouDep = Annotated[ContentUow, Depends(get_content_uow)]


def get_profile_update(uow: ContentUow) -> ProfilesUpdateUseCase:
    return ProfilesUpdateUseCase(uow=uow)


ProfileUpdateDepends = Annotated[
    ProfilesUpdateUseCase, Depends(get_profile_update)
]
