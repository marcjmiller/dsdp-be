"""Tests for Auth Routes"""
from fastapi import FastAPI
from fastapi.testclient import TestClient

from starlette.status import HTTP_404_NOT_FOUND


def test_get_user_roles(app: FastAPI, client: TestClient):
    """Test for get user roles"""
    response = client.get(app.url_path_for("auth:getUserRoles"))
    assert response.status_code != HTTP_404_NOT_FOUND
