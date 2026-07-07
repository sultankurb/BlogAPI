from fastapi import APIRouter

from src.presentation.api.content.comments_router import comments_router
from src.presentation.api.content.posts_router import posts_router
from src.presentation.api.content.profiles_router import profiles_router

content_router = APIRouter(
    prefix="/content",
    tags=["content"],
)
content_router.include_router(profiles_router)
content_router.include_router(posts_router)
content_router.include_router(comments_router)