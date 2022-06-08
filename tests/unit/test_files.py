"""Tests for the files endpoints"""
import pytest
from fastapi import UploadFile
from mock import MagicMock
from api.routes.files import download, list_objects, upload, delete
from api.models.file_info import FileReleaseType
from api.config import logger  # pylint: disable=unused-import

BUCKET = "bucket"


@pytest.mark.asyncio
async def test_download(mocker):
    """Tests download function"""
    expected = "test"
    mock = mocker.patch("api.routes.files.s3.get_object")
    await download("test")
    mock.assert_called_with(Bucket=BUCKET, Key=expected)


@pytest.mark.asyncio
async def test_list_objects(mocker):
    """Tests list endpoint"""
    mock = mocker.patch("api.routes.files.s3.list_objects", MagicMock())
    await list_objects()
    mock.assert_called_with(Bucket=BUCKET)


@pytest.mark.asyncio
async def test_upload_objects(mocker):
    """Tests upload endpoint"""
    expected = UploadFile(filename="test")
    mock = mocker.patch("api.routes.files.s3.upload_fileobj", MagicMock())
    await upload(expected)
    mock.assert_called_with(
        Fileobj=expected.file,
        Bucket=BUCKET,
        Key=expected.filename,
        ExtraArgs={"Metadata": {"release_type": ""}},
    )


@pytest.mark.asyncio
async def test_upload_objects_with_metadata(mocker):
    """Tests upload endpoint with release type metadata"""
    expected = UploadFile(filename="test")
    release_type = FileReleaseType.OUT_OF_CYCLE
    mock = mocker.patch("api.routes.files.s3.upload_fileobj", MagicMock())
    await upload(expected, release_type)
    mock.assert_called_with(
        Fileobj=expected.file,
        Bucket=BUCKET,
        Key=expected.filename,
        ExtraArgs={"Metadata": {"release_type": release_type.value}},
    )


@pytest.mark.asyncio
async def test_delete(mocker):
    """Tests delete endpoint"""
    expected = "test"
    mock = mocker.patch("api.routes.files.s3.delete_object", MagicMock())
    await delete("test")
    mock.assert_called_with(Bucket=BUCKET, Key=expected)
