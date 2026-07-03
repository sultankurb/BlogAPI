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
from src.domain.identity.use_cases.uow import IdentityUow
from src.infrastructure.database import session_factory
from src.infrastructure.notifications.depends import get_notification_service
from src.presentation.api.dependecies import RedisDep

security = HTTPBearer()

def get_identity_uow() -> IdentityUow:
    return IdentityUow(session=session_factory)

IdentityUowDep = Annotated[IdentityUow, Depends(get_identity_uow)]

async def get_current_user_id(
    redis: RedisDep,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials
    try:
        jwt_service = JWTService(redis=redis)
        payload = jwt_service.decode_token(token=token)
        return payload

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def get_register_use_case(
    uow: IdentityUowDep,
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
    uow: IdentityUowDep,
):
    password = PasswordService()
    jwt_service = JWTService(redis=redis)
    return LoginUseCase(
        uow=uow, password_service=password, jwt_service=jwt_service
    )


UserLoginDepends = Annotated[LoginUseCase, Depends(get_login_use_case)]


def get_user_use_case(uow: IdentityUowDep):
    return GetCurrentUserUseCase(uow=uow)


GetCurrentUserDepends = Annotated[
    GetCurrentUserUseCase, Depends(get_user_use_case)
]


async def check_user_black_wall(
    redis: RedisDep,
    user: dict = Depends(get_current_user_id),
) -> dict:
    check = await redis.get(f"black:list:{user["sub"]}")
    if check is not None:
        raise HTTPException(status_code=403, detail="User already blacklisted")
    return user


UserDepends = Annotated[dict, Depends(check_user_black_wall)]


def get_activate_service(
    uow: IdentityUowDep,
    redis: RedisDep,
) -> UpdateStatusUseCase:
    return UpdateStatusUseCase(uow=uow, redis=redis)


UserActivateDepends = Annotated[
    UpdateStatusUseCase, Depends(get_activate_service)
]
