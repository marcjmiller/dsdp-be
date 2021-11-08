from fastapi import FastAPI
from backend.api.routes.api import router as api_router


def get_application() -> FastAPI:
  application = FastAPI(openapi_prefix="/api")
  application.include_router(api_router)


app = get_application()
