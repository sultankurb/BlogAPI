from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.infrastructure.lifespan import lifespan
from src.presentation.api.handlers import handler, setup_exception_handlers

app = FastAPI(lifespan=lifespan)
setup_exception_handlers(app)
app.include_router(handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
