from fastapi import APIRouter

from .files import router as files_router
from .auth import router as auth_router


router = APIRouter()

router.include_router(files_router, tags=["files"], prefix="/files")
router.include_router(auth_router, tags=["auth"], prefix="/auth")
