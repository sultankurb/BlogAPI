from fastapi import FastAPI

from src.presentation.api.handlers import handler, setup_exception_handlers

app = FastAPI()
setup_exception_handlers(app)
app.include_router(handler)
