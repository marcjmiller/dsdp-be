import os
import logging
from fastapi import APIRouter, UploadFile
from starlette.responses import StreamingResponse, Response
import boto3
from botocore.exceptions import ClientError

files_router = APIRouter()

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
    endpoint_url="http://" + MINIO_URL,
)


def bucket_exists(bucket_name: str) -> bool:
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if not bucket_exists(MINIO_BUCKET):
    logging.info('creating bucket %s', MINIO_BUCKET)
    s3.create_bucket(Bucket=MINIO_BUCKET)


@files_router.get("", name="files:getFile", response_class=StreamingResponse)
async def download(name: str) -> StreamingResponse:
    logging.info(s3.get_object(Bucket=MINIO_BUCKET, Key=name)['Body'].iter_chunks(8096))
    res = Response(content=s3.get_object(Bucket=MINIO_BUCKET, Key=name)['Body'].iter_chunks(8096))
    return res


@files_router.get("/list", name="files:list")
async def list_objects():
    return s3.list_objects(Bucket=MINIO_BUCKET)


@files_router.post("", name="files:create")
async def create(file: UploadFile) -> bool:
    try:
        s3.upload_fileobj(Fileobj=file.file, Bucket=MINIO_BUCKET, Key=file.filename)
    except ClientError as e:
        logging.error(e)
        return False
    return True


@files_router.delete("", name="files:delete")
async def delete(name: str):
    try:
        s3.delete_object(Bucket=MINIO_BUCKET, Key=name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

