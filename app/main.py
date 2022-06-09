"""
Main Module
"""
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Secweb.ContentSecurityPolicy import ContentSecurityPolicy
from app.api import api
from app.core.config import get_settings
from app.core import logger  # pylint: disable=unused-import

settings = get_settings()


def get_application() -> FastAPI:
    """
    DocString
    """
    application = FastAPI()
    if settings.DEVELOPMENT:
        origins = ["*"]

        application.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    application.add_middleware(
        ContentSecurityPolicy,
        Option={
            "default-src": ["'self'"],
            "connect-src": ["'self'"],
            "form-action": ["'none'"],
        },
        script_nonce=False,
        style_nonce=False,
    )

    application.include_router(api.router, prefix="/api")
    return application


app = get_application()
