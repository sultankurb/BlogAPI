from typing import Annotated

from fastapi import Depends

from src.domain.identity.services.jwt_service import JWTService
from src.domain.identity.services.password_service import (
    PasswordService,
    get_password_service,
)
from src.domain.identity.use_cases.login import LoginUseCase
from src.domain.identity.use_cases.register import UsersRegisterUseCase
from src.domain.identity.use_cases.get_users import GetCurrentUserUseCase
from src.infrastructure.database import UnitOfWork, session_factory


def get_uow() ->UnitOfWork:
    return UnitOfWork(session_maker=session_factory)

def get_jwt() -> JWTService:
    return JWTService()


UoWDep = Annotated[UnitOfWork, Depends(get_uow)]
PasswordDep = Annotated[PasswordService, Depends(get_password_service)]
JWTDep = Annotated[JWTService, Depends(get_jwt)]


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
        uow: UoWDep,
        jwt_service: JWTDep
):
    return GetCurrentUserUseCase(jwt_service=jwt_service, ouw=uow)

GetCurrentUserUseCaseDepends = Annotated[
    GetCurrentUserUseCase,
    Depends(get_user_use_case)
]