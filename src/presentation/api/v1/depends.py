from typing import Annotated

from fastapi import Depends

from src.domain.identity.services.password_service import (
    PasswordService,
    get_password_service,
)
from src.domain.identity.use_cases.register import UsersRegisterUseCase
from src.infrastructure.database import UnitOfWork, session_factory


async def get_uow() ->UnitOfWork:
    return UnitOfWork(session_maker=session_factory)

UoWDep = Annotated[UnitOfWork, Depends(get_uow)]



def get_register_use_case(
    uow: UoWDep,
    hasher: PasswordService = Depends(get_password_service),
) -> UsersRegisterUseCase:
    return UsersRegisterUseCase(uow=uow, password_service=hasher)

UserRegisterCase = Annotated[
    UsersRegisterUseCase,
    Depends(get_register_use_case)
]