"""Tests for Auth Routes"""
from fastapi import FastAPI
from fastapi.testclient import TestClient
import jwt
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from app.api.deps import get_s3_client


fake_token = jwt.encode(
    {"name": "ClintIsACat", "group-full": "/Platform One/gvsc/IL2/roles/admin", "preferred_username": "nobody.ctr"},
    "superSecret",
)

async def fake1_boto_client():
    class mock_client:
        def upload_fileobj(*args, **kwargs):
            return {}
        def list_objects(*args, **kwargs):
            return {"Contents": [{"Key": "whats.your.name"}, {"Key": "ezekiel"}]}
    return mock_client


def test_whoami(app: FastAPI, client: TestClient):
    """Test for get user roles"""
    app.dependency_overrides[get_s3_client] = fake1_boto_client
    response = client.get(
        app.url_path_for("auth:whoami"),
        headers={"Authorization": f"Bearer {fake_token}"},
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"isAdmin": True, "name": "ClintIsACat", "preferredUsername": "nobody.ctr"}


def test_whoami_with_bad_token(app: FastAPI, client: TestClient):
    """Test for get user roles"""
    app.dependency_overrides[get_s3_client] = fake1_boto_client
    response = client.get(
        app.url_path_for("auth:whoami"), headers={"Authorization": f"Bearer BadToken"}
    )
    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Not a valid token"}

def test_list_admins(app: FastAPI, client: TestClient):
    """Test for getting list of admins"""
    app.dependency_overrides[get_s3_client] = fake1_boto_client
    response = client.get(app.url_path_for("auth:admins"))
    assert response.status_code == HTTP_200_OK
    assert response.json() == ["whats.your.name", "ezekiel"]