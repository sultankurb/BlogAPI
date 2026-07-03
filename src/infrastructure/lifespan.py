from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.domain.identity.services.password_service import PasswordService
from src.domain.identity.use_cases import RootUserUseCase, SeedRolesUseCase
from src.domain.identity.use_cases.uow import IdentityUow
from src.infrastructure.database import session_factory
from src.infrastructure.redis import connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection.init_redis_client()
    identity_uow = IdentityUow(session=session_factory)
    roles_use_case = SeedRolesUseCase(identity_uow)
    users_use_case = RootUserUseCase(
        uow=identity_uow,
        password_service=PasswordService()
    )
    await roles_use_case.execute(settings.DEFAULT_USERS_ROLES)
    await users_use_case.execute(
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD,
        username=settings.ADMIN_USERNAME,
    )
    yield
    if connection.redis_client:
        await connection.redis_client.aclose()
