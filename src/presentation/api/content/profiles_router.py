from fastapi import APIRouter

profiles_router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)
