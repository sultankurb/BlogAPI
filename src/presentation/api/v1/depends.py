from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.identity.services.jwt_service import JWTService
from src.domain.identity.services.password_service import (
    PasswordService,
    get_password_service,
)
from src.domain.identity.use_cases.get_users import GetCurrentUserUseCase
from src.domain.identity.use_cases.login import LoginUseCase
from src.domain.identity.use_cases.register import UsersRegisterUseCase
from src.infrastructure.database import UnitOfWork, session_factory


def get_uow() ->UnitOfWork:
    return UnitOfWork(session_maker=session_factory)

def get_jwt() -> JWTService:
    return JWTService()



UoWDep = Annotated[UnitOfWork, Depends(get_uow)]
PasswordDep = Annotated[PasswordService, Depends(get_password_service)]
JWTDep = Annotated[JWTService, Depends(get_jwt)]
security = HTTPBearer()


async def get_current_user_id(
    jwt_service: JWTDep,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    token = credentials.credentials
    try:
        payload = jwt_service.decode_token(token=token)
        user_id = int(payload.get("sub"))
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def get_register_use_case(
    uow: UoWDep,
    hasher: PasswordDep
) -> UsersRegisterUseCase:
    return UsersRegisterUseCase(uow=uow, password_service=hasher)

UserRegisterCaseDepends = Annotated[
    UsersRegisterUseCase,
    Depends(get_register_use_case)
]

def get_login_use_case(
        uow: UoWDep,
        password: PasswordDep,
        jwt_service: JWTDep
):
    return LoginUseCase(
        uow=uow,
        password_service=password,
        jwt_service=jwt_service
    )

UserLoginUseCaseDepends = Annotated[LoginUseCase, Depends(get_login_use_case)]

def get_user_use_case(
        uow: UoWDep
):
    return GetCurrentUserUseCase(ouw=uow)

GetCurrentUserUseCaseDepends = Annotated[
    GetCurrentUserUseCase,
    Depends(get_user_use_case)
]
UserPKDepends = Annotated[int, Depends(get_current_user_id)]
