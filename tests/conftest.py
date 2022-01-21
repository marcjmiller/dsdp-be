import os
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from minio import Minio

MINIO_ENDPOINT = "minio:9000" if os.getenv("CI") else "localhost:9000"


@pytest_asyncio.fixture(autouse=True)
def init_minio():
    c = Minio(MINIO_ENDPOINT, "minio", "minio123", secure=False)
    if not c.bucket_exists("test"):
        c.make_bucket("test")
    yield


@pytest_asyncio.fixture
def app() -> FastAPI:
    from main import get_application
    import logger

    return get_application()


@pytest_asyncio.fixture
def client(app: FastAPI) -> TestClient:
    yield TestClient(app)
