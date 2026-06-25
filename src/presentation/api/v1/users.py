from fastapi import APIRouter, Response

from src.domain.identity.schemas.token import Token
from src.domain.identity.schemas.users import LoginSchemas, UsersCreateModel
from src.presentation.api.v1.depends import (
    GetCurrentUserUseCaseDepends,
    UserLoginUseCaseDepends,
    UserRegisterCaseDepends,
)

users_router = APIRouter(
    prefix="/users",
)


@users_router.post("/register/new/user")
async def register_new_user(
        user: UsersCreateModel,
        user_service: UserRegisterCaseDepends
):
    user_pk = await  user_service.execute(user=user)
    return {"user": user_pk}

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


@users_router.post(path="/get/current/user")
async def get_current_user(
        token: str,
        user_service: GetCurrentUserUseCaseDepends,
):
    user = await user_service.execute(token=token)
    return user
