import os
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient

@pytest_asyncio.fixture
def app() -> FastAPI:
    from main import get_application
    import logger

    return get_application()


@pytest_asyncio.fixture
def client(app: FastAPI) -> TestClient:
    yield TestClient(app)
