from fastapi import FastAPI

from src.infrastructure.lifespan import lifespan
from src.presentation.api.handlers import handler, setup_exception_handlers

app = FastAPI(lifespan=lifespan)
setup_exception_handlers(app)
app.include_router(handler)
