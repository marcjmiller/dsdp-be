from fastapi import FastAPI
from api.routes.api import router as api_router


def get_application() -> FastAPI:
  application = FastAPI()
  application.include_router(api_router, prefix="/api")
  return application


app = get_application()
