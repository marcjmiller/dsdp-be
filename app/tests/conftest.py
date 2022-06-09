"""
Configure test fixtures
"""
# pylint: disable=redefined-outer-name
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import get_application


@pytest.fixture
def app() -> FastAPI:
    """Returns a new api app for testing"""
    return get_application()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create Test wrapper for application"""
    yield TestClient(app)
