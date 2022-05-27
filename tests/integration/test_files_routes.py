"""Tests for files routes"""
from fastapi import FastAPI
from fastapi.testclient import TestClient

from starlette.status import HTTP_404_NOT_FOUND


def test_get_bucket_items(app: FastAPI, client: TestClient):
    """Test for get bucket items"""
    response = client.get(app.url_path_for("files:list"))
    assert response.status_code != HTTP_404_NOT_FOUND


def test_add_bucket_items(app: FastAPI, client: TestClient):
    """Test for add bucket items"""
    response = client.post(app.url_path_for("files:upload"))
    assert response.status_code != HTTP_404_NOT_FOUND


def test_download_file(app: FastAPI, client: TestClient):
    """Test for downloading items"""
    response = client.get(app.url_path_for("files:download"))
    assert response.status_code != HTTP_404_NOT_FOUND


def test_delete_file(app: FastAPI, client: TestClient):
    """Test for get Delete items"""
    response = client.get(app.url_path_for("files:delete"))
    assert response.status_code != HTTP_404_NOT_FOUND
