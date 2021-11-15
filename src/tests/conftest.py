import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

@pytest.fixture
def app() -> FastAPI:
  from src.main import get_application
  print(get_application())
  return get_application()

@pytest.fixture
def client(app: FastAPI) -> TestClient:
  yield TestClient(app)
