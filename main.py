from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.domain.identity.services.password_service import PasswordService
from src.domain.identity.use_cases.seed_roles import SeedRolesUseCase
from src.domain.identity.use_cases.seed_user import SeedUserUseCase
from src.infrastructure.database import UnitOfWork, session_factory
from src.infrastructure.redis import connection
from src.presentation.api.handlers import handler, setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection.init_redis_client()
    uow = UnitOfWork(session_maker=session_factory)
    roles_use_case = SeedRolesUseCase(uow)
    users_use_case = SeedUserUseCase(uow, password_service=PasswordService())
    await roles_use_case.execute(settings.DEFAULT_USERS_ROLES)
    await users_use_case.execute(
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD,
        username=settings.ADMIN_USERNAME
    )
    yield
    if connection.redis_client:
        await connection.redis_client.aclose()


# Подключаем lifespan к приложению
app = FastAPI(lifespan=lifespan)
setup_exception_handlers(app)
app.include_router(handler)
