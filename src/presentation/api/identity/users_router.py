from fastapi import APIRouter, BackgroundTasks, Response, status

from src.domain.identity.schemas.token import Token
from src.domain.identity.schemas.users import (
    LoginSchemas,
    UserReadModel,
    UsersCreateModel,
)
from src.presentation.api.identity.dependencies import (
    GetCurrentUserUseCaseDepends,
    UserActivateUseCaseDepends,
    UserLoginUseCaseDepends,
    UserPKDepends,
    UserRegisterCaseDepends,
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
        user_service: UserRegisterCaseDepends,
        background_tasks: BackgroundTasks,
):
    user = await  user_service.execute(
        user=user,
        background_tasks=background_tasks
    )
    return user

@users_router.post(path="/login", response_model=Token)
async def login_user(
        login_schema: LoginSchemas,
        user_login: UserLoginUseCaseDepends,
        response: Response,
):
    tokens = await user_login.execute(
        email=login_schema.email,
        password=login_schema.password
    )
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True
    )
    return tokens


@users_router.post(path="/get/current/user/", response_model=UserReadModel)
async def get_current_user(
        user_pk: UserPKDepends,
        user_service: GetCurrentUserUseCaseDepends,
):
    user = await user_service.execute(user_pk=user_pk)
    return user

@users_router.post(path="/verify/current/user/")
async def verify_user(
        code: int,
        user_service: UserActivateUseCaseDepends,
        user_pk: UserPKDepends
):
    await user_service.execute(code=code, user_pk=user_pk)
