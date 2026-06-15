from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from src.config.exception import (
    ApplicationException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
)


def setup_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException):
        # Сюда прилетит и юзер, и пост, и коммент. Код один и тот же.
        return JSONResponse(status_code=404, content={"error": exc.message})

    @app.exception_handler(ConflictException)
    async def conflict_handler(request: Request, exc: ConflictException):
        return JSONResponse(status_code=409, content={"error": exc.message})

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(request: Request, exc: ForbiddenException):
        return JSONResponse(status_code=403, content={"error": exc.message})

    # Фоллбэк для всех остальных ApplicationException
    @app.exception_handler(ApplicationException)
    async def application_error_handler(
        request: Request, exc: ApplicationException
    ):
        return JSONResponse(status_code=400, content={"error": exc.message})

handler = APIRouter(
    prefix="/api",
)
