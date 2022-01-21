from fastapi import APIRouter

from .files import files_router
from .auth import auth_router


router = APIRouter()

router.include_router(files_router, tags=["files"], prefix="/files")
router.include_router(auth_router, tags=["auth"])
