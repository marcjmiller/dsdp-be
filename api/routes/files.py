"""
Files endpoints
"""
import logging
import os
from typing import List
import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, UploadFile
from starlette.responses import StreamingResponse

from api.models.file_info import FileInfo, parse_s3_contents

files_router = APIRouter()

CHUNK_SIZE = 8 * 1024 * 1024

MINIO_BUCKET = os.getenv("MINIO_BUCKET_NAME", "bucket")
MINIO_HOST = os.getenv("MINIO_HOST", "localhost")
MINIO_PORT = os.getenv("MINIO_PORT", "9000")
MINIO_PROTOCOL = os.getenv("MINIO_PROTOCOL", "http")
MINIO_URL = f"{MINIO_HOST}:{MINIO_PORT}"
MINIO_REGION = os.getenv("MINIO_REGION")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio123")

s3 = boto3.client(
    "s3",
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    endpoint_url=MINIO_PROTOCOL + "://" + MINIO_URL,
)


def bucket_exists(bucket_name: str) -> bool:
    """Check if the S3 Bucket exists"""
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as error:
        logging.error(error)
        return False
    return True


if not bucket_exists(MINIO_BUCKET):
    s3.create_bucket(Bucket=MINIO_BUCKET)


@files_router.get("", name="files:download")
async def download(name: str):
    """Downloads a file from a bucket and streams it to the client"""
    return StreamingResponse(
        s3.get_object(Bucket=MINIO_BUCKET, Key=name)["Body"].iter_chunks(CHUNK_SIZE)
    )


@files_router.get("/list", name="files:list")
async def list_objects() -> List[FileInfo]:
    """Lists all bucket objects"""
    objects = s3.list_objects(Bucket=MINIO_BUCKET)
    return [parse_s3_contents(obj) for obj in objects.get("Contents", [])]


@files_router.post("", name="files:upload")
async def upload(file: UploadFile) -> bool:
    """Uploads a file to the S3 bucket"""
    try:
        s3.upload_fileobj(Fileobj=file.file, Bucket=MINIO_BUCKET, Key=file.filename)
    except ClientError as error:
        logging.error(error)
        return False
    return True


@files_router.delete("", name="files:delete")
async def delete(name: str):
    """Deletes a file from a Bucket"""
    try:
        s3.delete_object(Bucket=MINIO_BUCKET, Key=name)
    except ClientError as error:
        logging.error(error)
        return False
    return True
