from fastapi import APIRouter

from src.domain.content.schemas import ProfileUpdatedModel
from src.presentation.api.content.dependencies import ProfileUpdateDepends
from src.presentation.api.identity.dependencies import UserPKDepends

profiles_router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)


@profiles_router.patch(path="/update/profile/")
async def update_user_profile(
    pk: UserPKDepends,
    profile: ProfileUpdatedModel,
    profile_service: ProfileUpdateDepends,
):
    result = await profile_service.execute(pk=pk, data=profile)
    return result
