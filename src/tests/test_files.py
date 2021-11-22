from fastapi import FastAPI
from fastapi.testclient import TestClient

from starlette.status import HTTP_404_NOT_FOUND


class TestFilesRoutes:
  def test_get_bucket_items(self, app: FastAPI, client: TestClient):
    response = client.get(app.url_path_for("files:list"))
    assert response.status_code != HTTP_404_NOT_FOUND
    assert len(response.json()) > 0

  def test_add_bucket_items(self, app: FastAPI, client: TestClient):
    response = client.post(app.url_path_for("files:create"))
    assert response.status_code != HTTP_404_NOT_FOUND
    # TODO: Finish test by adding file and testing if it is there