"""
Files endpoints
"""
import logging
from typing import List, Generator

from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, File, status, HTTPException, UploadFile, Form

from app.models.file_info import FileInfo, FileReleaseType, parse_s3_contents
from app.api.deps import get_s3_client
from app.core.config import get_settings
from starlette.responses import StreamingResponse

CHUNK_SIZE = 8 * 1024 * 1024

settings = get_settings()

router = APIRouter()


def __get_and_attach_metadata(
    file,
    s3: Generator,
) -> dict:
    """Gets metadata about an object in s3 and attaches it to the file"""
    return {
        **file,
        "metadata": s3.head_object(Bucket=settings.MINIO_BUCKET_NAME, Key=file["Key"])[
            "Metadata"
        ],
    }


@router.get("", name="files:download")
async def download(name: str, s3=Depends(get_s3_client)):
    """
    Downloads a file
    """
    return StreamingResponse(
        s3.get_object(Bucket=settings.MINIO_BUCKET_NAME, Key=name)["Body"].iter_chunks(
            CHUNK_SIZE
        )
    )


@router.get("/list", name="files:list")
async def list_objects(s3=Depends(get_s3_client)) -> List[FileInfo]:
    """
    Lists all bucket objects
    """
    objects = s3.list_objects(Bucket=settings.MINIO_BUCKET_NAME)
    objects_with_metadata = [
        __get_and_attach_metadata(obj, s3) for obj in objects.get("Contents", [])
    ]
    return [parse_s3_contents(obj) for obj in objects_with_metadata]


@router.post("", name="files:upload", status_code=status.HTTP_201_CREATED)
async def upload(
    s3=Depends(get_s3_client),
    file: UploadFile = File(...),
    release_type: FileReleaseType = Form(None),
):
    """Uploads a file to the S3 bucket"""
    release_value = getattr(release_type, "value", "")
    try:
        s3.upload_fileobj(
            Fileobj=file.file,
            Bucket=settings.MINIO_BUCKET_NAME,
            Key=file.filename,
            ExtraArgs={"Metadata": {"release_type": release_value}},
        )
        return FileInfo(
            name=file.filename, size=0, metadata={"release_type": release_value}
        )
    except ClientError as error:
        raise HTTPException(
            status_code=500, detail=f"Something went wrong with s3:\n\t{error}"
        )


@router.delete("", name="files:delete")
async def delete(
    name: str,
    s3=Depends(get_s3_client),
):
    """
    Deletes a file from a Bucket
    """
    try:
        s3.delete_object(Bucket=settings.MINIO_BUCKET_NAME, Key=name)
    except ClientError as error:
        logging.error(error)
        return False
    return True
