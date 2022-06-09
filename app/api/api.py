"""
Router for the API
"""
from fastapi import APIRouter

from app.api.endpoints import files, auth

router = APIRouter()

router.include_router(files.router, tags=["files"], prefix="/files")
router.include_router(auth.router, tags=["auth"])
