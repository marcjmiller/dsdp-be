import pytest
from fastapi import UploadFile
from api.routes.files import download, list_objects, create, delete
from mock import MagicMock

BUCKET = "bucket"


@pytest.mark.asyncio
async def test_download(mocker):
    expected = "test"
    mock = mocker.patch("backend.api.routes.files.Minio.presigned_get_object", MagicMock())
    await download("test")
    mock.assert_called_with(BUCKET, expected)


@pytest.mark.asyncio
async def test_list_objects(mocker):
    mock = mocker.patch("backend.api.routes.files.Minio.list_objects", MagicMock())
    await list_objects()
    mock.assert_called_with(BUCKET)


@pytest.mark.asyncio
async def test_list_objects(mocker):
    expected = [UploadFile(filename="test")]
    mock = mocker.patch("backend.api.routes.files.Minio.fput_object", MagicMock())
    await create(expected)
    mock.assert_called_with(BUCKET, expected[0].filename, expected[0].file.fileno())


@pytest.mark.asyncio
async def test_delete(mocker):
    expected = "test"
    mock = mocker.patch("backend.api.routes.files.Minio.remove_object", MagicMock())
    await delete("test")
    mock.assert_called_with(BUCKET, expected)
