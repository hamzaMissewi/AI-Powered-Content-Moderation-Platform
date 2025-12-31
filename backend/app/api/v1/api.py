# backend/app/api/v1/api.py
from fastapi import APIRouter

from app.api.v1.endpoints import users, auth, content, moderate

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(moderate.router, prefix="/moderate", tags=["moderation"])