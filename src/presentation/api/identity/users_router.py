from fastapi import APIRouter, BackgroundTasks, status

from src.domain.identity.schemas.token import Token
from src.domain.identity.schemas.users import (
    LoginSchemas,
    UserReadModel,
    UsersCreateModel,
)
from src.presentation.api.identity.dependencies import (
    GetCurrentUserDepends,
    UserActivateDepends,
    UserDepends,
    UserLoginDepends,
    UserRefreshJWTDepends,
    UserRegisterDepends,
)

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@users_router.post(
    path="/register/new/user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserReadModel,
)
async def register_new_user(
    user: UsersCreateModel,
    user_service: UserRegisterDepends,
    background_tasks: BackgroundTasks,
):
    user = await user_service.execute(
        user=user, background_tasks=background_tasks
    )
    return user


@users_router.post(path="/login", response_model=Token)
async def login_user(
    login_schema: LoginSchemas,
    user_login: UserLoginDepends,
):
    tokens = await user_login.execute(
        email=login_schema.email, password=login_schema.password
    )
    return tokens


@users_router.get(path="/get/current/user/", response_model=UserReadModel)
async def get_current_user(
    user_credentials: UserDepends,
    user_service: GetCurrentUserDepends,
):
    user = await user_service.execute(user_pk=int(user_credentials["sub"]))
    return user


@users_router.post(
    path="/verify/current/user/",
    status_code=status.HTTP_204_NO_CONTENT
)
async def verify_user(
    code: int, user_service: UserActivateDepends, user: UserDepends
):
    await user_service.execute(code=code, user_pk=int(user["sub"]))


@users_router.post(
    path="/refresh/tokens/",
    response_model=Token,
)
async def get_new_tokens(
        last_refresh_toke: str,
        refresh: UserRefreshJWTDepends
):
    tokens = await refresh.execute(refresh_toke=last_refresh_toke)
    return tokens
