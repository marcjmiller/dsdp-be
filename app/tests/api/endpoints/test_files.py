"""Tests for files Endpoints"""
import fastapi
import jwt
from fastapi import FastAPI
from fastapi.testclient import TestClient
from botocore.exceptions import ClientError
from starlette.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR

from app.api.deps import get_s3_client
from app.models.file_info import FileReleaseType

test_file = {"file": open("./app/tests/api/endpoints/hello.txt", "rb")}


async def fake1_boto_client():
    class mock_client:
        def upload_fileobj(*args, **kwargs):
            return {}
    return mock_client


def test_upload(app: FastAPI, client: TestClient):
    app.dependency_overrides[get_s3_client] = fake1_boto_client
    response = client.post(
        app.url_path_for("files:upload"),
        files=test_file,
        data={"release_type": FileReleaseType.OUT_OF_CYCLE.value},
    )
    assert response.status_code == HTTP_201_CREATED
    assert response.json() == {
        "metadata": {"release_type": FileReleaseType.OUT_OF_CYCLE.value},
        "name": "hello.txt",
        "size": 0,
        "isDownloading": False,
        "isUploading": False,
    }


async def fake_boto_client():
    class mock_client:
        def upload_fileobj(*args, **kwargs):
            raise ClientError({}, "s3")

    return mock_client


def test_failed_upload(app: fastapi, client: TestClient):
    app.dependency_overrides[get_s3_client] = fake_boto_client

    response = client.post(
        app.url_path_for("files:upload"),
        files=test_file,
        data={"response_type": FileReleaseType.OUT_OF_CYCLE.value},
    )
    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
