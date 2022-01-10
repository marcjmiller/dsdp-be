from fastapi import FastAPI
from fastapi.testclient import TestClient

from starlette.status import HTTP_404_NOT_FOUND


class TestFilesRoutes:
    def test_get_user_roles(self, app: FastAPI, client: TestClient):
        response = client.get(app.url_path_for("auth:getUserRoles"))
        assert response.status_code != HTTP_404_NOT_FOUND
