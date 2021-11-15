from fastapi import FastAPI
from fastapi.testclient import TestClient

from starlette.status import HTTP_404_NOT_FOUND
class TestFilesRoutes:
  def test_routes_exist(self, app: FastAPI, client: TestClient):
    res = client.get(app.url_path_for("files:hello"))
    assert res.status_code != HTTP_404_NOT_FOUND
    