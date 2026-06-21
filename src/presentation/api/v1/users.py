from fastapi import APIRouter

from src.domain.identity.schemas.users import UsersCreateModel
from src.presentation.api.v1.depends import UoWDep, UserRegisterCase

users_router = APIRouter(
    prefix="/users",
)


@users_router.post("/register/new/user")
async def register_new_user(
        user: UsersCreateModel,
        user_service: UserRegisterCase
):
    user_pk = await  user_service.execute(user=user)
    return {"user": user_pk}
