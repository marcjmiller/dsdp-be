"""
Configure test fixtures
"""
# pylint: disable=redefined-outer-name
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest_asyncio.fixture
def app() -> FastAPI:
    """Returns a new api app for testing"""
    from main import get_application
    from api.config import logger  # pylint: disable=unused-import

    return get_application()


@pytest_asyncio.fixture
def client(app: FastAPI) -> TestClient:
    """Create Test wrapper for application"""
    yield TestClient(app)
