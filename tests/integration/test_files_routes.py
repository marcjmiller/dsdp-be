from fastapi import FastAPI
from fastapi.testclient import TestClient

from starlette.status import HTTP_404_NOT_FOUND


class TestFilesRoutes:
    def test_get_bucket_items(self, app: FastAPI, client: TestClient):
        response = client.get(app.url_path_for("files:list"))
        assert response.status_code != HTTP_404_NOT_FOUND

    def test_add_bucket_items(self, app: FastAPI, client: TestClient):
        response = client.post(app.url_path_for("files:create"))
        assert response.status_code != HTTP_404_NOT_FOUND

    def test_download_file(self, app: FastAPI, client: TestClient):
        response = client.get(app.url_path_for("files:getFileURL"))
        assert response.status_code != HTTP_404_NOT_FOUND

    def test_delete_file(self, app: FastAPI, client: TestClient):
        response = client.get(app.url_path_for("files:delete"))
        assert response.status_code != HTTP_404_NOT_FOUND
