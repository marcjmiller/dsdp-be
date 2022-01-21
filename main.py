from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.api import router as api_router
import logger  # pylint: disable=unused-import


def get_application() -> FastAPI:
    application = FastAPI()
    origins = ["*"]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix="/api")
    return application


app = get_application()
