from fastapi import APIRouter

from src.presentation.api.identity.admins_router import admin_router
from src.presentation.api.identity.users_router import users_router

identity_router = APIRouter(
    prefix="/identity",
    tags=["identity"],
)
identity_router.include_router(router=users_router)
identity_router.include_router(router=admin_router)
