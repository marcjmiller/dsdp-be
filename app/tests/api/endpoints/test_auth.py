"""Tests for Auth Routes"""
from fastapi import FastAPI
from fastapi.testclient import TestClient
import jwt

from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK

fake_token = jwt.encode(
    {"name": "ClintIsACat", "group-full": "/Platform One/gvsc/IL2/roles/admin"},
    "superSecret",
)


def test_whoami(app: FastAPI, client: TestClient):
    """Test for get user roles"""
    response = client.get(
        app.url_path_for("auth:whoami"),
        headers={"Authorization": f"Bearer {fake_token}"},
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"isAdmin": True, "name": "ClintIsACat"}


def test_whoami_with_bad_token(app: FastAPI, client: TestClient):
    """Test for get user roles"""
    response = client.get(
        app.url_path_for("auth:whoami"), headers={"Authorization": f"Bearer BadToken"}
    )
    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Not a valid token"}
