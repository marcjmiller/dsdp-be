import pytest
from fastapi import UploadFile
from api.routes.files import download, list_objects, upload, delete
from mock import MagicMock
import logging

BUCKET = "bucket"


@pytest.mark.asyncio
async def test_download(mocker):
    expected = "test"
    mock = mocker.patch("api.routes.files.s3.get_object")
    await download("test")
    mock.assert_called_with(Bucket=BUCKET, Key=expected)


@pytest.mark.asyncio
async def test_list_objects(mocker):
    mock = mocker.patch("api.routes.files.s3.list_objects",MagicMock())
    print(f"*************{mock.__dict__.keys()}")
    #mock().return_value = {"Contents": []}
    await list_objects()
    mock.assert_called_with(Bucket=BUCKET)


@pytest.mark.asyncio
async def test_upload_objects(mocker):
    expected = UploadFile(filename="test")
    mock = mocker.patch("api.routes.files.s3.upload_fileobj", MagicMock())
    await upload(expected)
    mock.assert_called_with(Fileobj=expected.file, Bucket=BUCKET, Key=expected.filename)


@pytest.mark.asyncio
async def test_delete(mocker):
    expected = "test"
    mock = mocker.patch("api.routes.files.s3.delete_object", MagicMock())
    await delete("test")
    mock.assert_called_with(Bucket=BUCKET, Key=expected)
