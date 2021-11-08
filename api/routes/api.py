from fastapi import APIRouter

from backend.api.routes import files

router = APIRouter()

router.include_router(files.router, tags=["files"], prefix="/files")
