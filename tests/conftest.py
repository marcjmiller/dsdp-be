import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from minio import Minio


@pytest.fixture(autouse=True)
def init_minio():
    c = Minio("minio:9000", "minio", "minio123", secure=False)
    if not c.bucket_exists("test"):
        c.make_bucket("test")
    yield


@pytest.fixture
def app() -> FastAPI:
    from backend.main import get_application

    return get_application()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    yield TestClient(app)
