from functools import lru_cache
from typing import Optional
from xmlrpc.client import boolean
from pydantic import BaseSettings


class Settings(BaseSettings):
    DEVELOPMENT: Optional[boolean]
    MINIO_BUCKET_NAME: Optional[str]
    MINIO_HOST: Optional[str]
    MINIO_PORT: Optional[int]
    MINIO_PROTOCOL: Optional[str]
    MINIO_REGION: Optional[str]
    MINIO_ACCESS_KEY: Optional[str]
    MINIO_SECRET_KEY: Optional[str]
    MINIO_URL: Optional[str]
    MINIO_ENDPOINT_URL: Optional[str]
    class Config:
        case_sensitive = True

@lru_cache
def get_settings():
    settings = Settings()
    if not settings.MINIO_BUCKET_NAME:
        settings.MINIO_BUCKET_NAME = "bucket"
    if not settings.MINIO_HOST:
        settings.MINIO_HOST = "localhost"
    if not settings.MINIO_PORT:
        settings.MINIO_PORT = 9000
    if not settings.MINIO_PROTOCOL:
        settings.MINIO_PROTOCOL = "http"
    if not settings.MINIO_ACCESS_KEY:
        settings.MINIO_ACCESS_KEY = "minio"
    if not settings.MINIO_SECRET_KEY:
        settings.MINIO_SECRET_KEY = "minio123"
    if not settings.MINIO_URL:
        settings.MINIO_URL = f"{settings.MINIO_HOST}:{settings.MINIO_PORT}"
    if not settings.MINIO_ENDPOINT_URL:
        settings.MINIO_ENDPOINT_URL=f"{settings.MINIO_PROTOCOL}://{settings.MINIO_URL}"
    return settings
