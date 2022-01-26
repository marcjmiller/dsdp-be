import os
import logging
from typing import List
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import RedirectResponse
from minio import Minio
from starlette.responses import FileResponse
from boto3 import client

files_router = APIRouter()

MINIO_BUCKET = os.getenv("MINIO_BUCKET_NAME", "bucket")
MINIO_HOST = os.getenv("MINIO_HOST", "localhost")
MINIO_PORT = os.getenv("MINIO_PORT", "9000")
MINIO_PROTOCOL = os.getenv("MINIO_PROTOCOL", "http")
MINIO_URL = f"{MINIO_HOST}:{MINIO_PORT}"
MINIO_REGION = os.getenv("MINIO_REGION")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio123")


def get_s3_client():
    if os.getenv("MINIO_SECRET_KEY", "minio123"):
        return client(
            "s3",
            endpoint_url=f"{MINIO_PROTOCOL}://{MINIO_URL}",
            region_name=MINIO_REGION,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY
        )
    else:
        return client(
            "s3",
            region_name=MINIO_REGION,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY
        )

s3 = get_s3_client()

mc = Minio(
    MINIO_URL,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    region=MINIO_REGION,
    secure=MINIO_PROTOCOL == "https",
)

if not mc.bucket_exists(MINIO_BUCKET):
    mc.make_bucket(MINIO_BUCKET)


@files_router.get("/get", name="files:getFile")
async def download(name: str) -> FileResponse:
    file = mc.fget_object(MINIO_BUCKET, name, name)
    return FileResponse(file._object_name)


@files_router.get("", name="files:getFileURL", response_class=RedirectResponse)
async def download(name: str) -> RedirectResponse:
    return s3.generate_presigned_url('get_object',
                                     Params={'Bucket': MINIO_BUCKET,
                                             'Key': name})


@files_router.get("/list", name="files:list")
async def list_objects():
    return mc.list_objects(MINIO_BUCKET)


@files_router.post("", name="files:create")
async def create(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        results.append(mc.fput_object(MINIO_BUCKET, file.filename, file.file.fileno()))
    return results


@files_router.delete("", name="files:delete")
async def delete(name: str):
    return mc.remove_object(MINIO_BUCKET, name)
