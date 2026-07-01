from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.identity.services import (
    JWTService,
    PasswordService,
    VerificationService,
)
from src.domain.identity.use_cases import (
    GetCurrentUserUseCase,
    LoginUseCase,
    RegisterUseCase,
    UpdateStatusUseCase,
)
from src.infrastructure.notifications.depends import get_notification_service
from src.presentation.api.dependecies import RedisDep, UoWDep

security = HTTPBearer()


async def get_current_user_id(
    redis: RedisDep,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    token = credentials.credentials
    try:
        jwt_service = JWTService(redis=redis)
        payload = jwt_service.decode_token(token=token)
        user_id = int(payload["sub"])
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def get_register_use_case(
    uow: UoWDep,
    redis: RedisDep,
) -> RegisterUseCase:
    hasher = PasswordService()
    verify_service = VerificationService(
        notification=get_notification_service(), redis=redis
    )
    return RegisterUseCase(
        uow=uow,
        password_service=hasher,
        verification_service=verify_service,
    )


UserRegisterDepends = Annotated[
    RegisterUseCase, Depends(get_register_use_case)
]


def get_login_use_case(
    redis: RedisDep,
    uow: UoWDep,
):
    password = PasswordService()
    jwt_service = JWTService(redis=redis)
    return LoginUseCase(
        uow=uow, password_service=password, jwt_service=jwt_service
    )


UserLoginDepends = Annotated[LoginUseCase, Depends(get_login_use_case)]


def get_user_use_case(uow: UoWDep):
    return GetCurrentUserUseCase(uow=uow)


GetCurrentUserDepends = Annotated[
    GetCurrentUserUseCase, Depends(get_user_use_case)
]


async def check_user_black_wall(
    redis: RedisDep,
    user_pk: int = Depends(get_current_user_id),
):
    check = await redis.get(f"black:list:{user_pk}")
    if check is not None:
        raise HTTPException(status_code=403, detail="User already blacklisted")
    return user_pk


UserPKDepends = Annotated[int, Depends(check_user_black_wall)]


def get_activate_service(
    uow: UoWDep,
    redis: RedisDep,
) -> UpdateStatusUseCase:
    return UpdateStatusUseCase(uow=uow, redis=redis)


UserActivateDepends = Annotated[
    UpdateStatusUseCase, Depends(get_activate_service)
]
