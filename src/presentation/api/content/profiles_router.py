from fastapi import APIRouter

from src.domain.content.schemas import ProfileUpdatedModel
from src.presentation.api.content.dependencies import ProfileUpdateDepends
from src.presentation.api.identity.dependencies import UserDepends

profiles_router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)


@profiles_router.patch(path="/update/profile/")
async def update_user_profile(
    user: UserDepends,
    profile: ProfileUpdatedModel,
    profile_service: ProfileUpdateDepends,
):
    result = await profile_service.execute(pk=int(user['sub']), data=profile)
    return result
