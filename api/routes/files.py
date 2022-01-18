import os
from typing import List
from fastapi import APIRouter, UploadFile, File
from minio import Minio
from starlette.responses import FileResponse


router = APIRouter()

MINIO_BUCKET = os.getenv("MINIO_BUCKET_NAME", "bucket")
MINIO_HOST = os.getenv("MINIO_HOST", "localhost")
MINIO_PORT = os.getenv("MINIO_PORT", "9000")
MINIO_PROTOCOL = os.getenv("MINIO_PROTOCOL", "http")
MINIO_URL = f"{MINIO_HOST}:{MINIO_PORT}"
MINIO_REGION = os.getenv("MINIO_REGION")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio123")

try:
    print(
        f"URL: {MINIO_URL}, Bucket: {MINIO_BUCKET}, Region: {MINIO_REGION}, {MINIO_PROTOCOL == 'https'}"
    )

    mc = Minio(
        MINIO_URL,
        MINIO_ACCESS_KEY,
        MINIO_SECRET_KEY,
        region=MINIO_REGION,
        secure=MINIO_PROTOCOL == "https",
    )

    if not mc.bucket_exists(MINIO_BUCKET):
        mc.make_bucket(MINIO_BUCKET)
except Exception as exception:
    print(f"Bucket: {MINIO_BUCKET}, \nMinio_URL: {MINIO_URL}, \nException: {exception}")
    raise exception


@router.get("", name="files:getFile")
async def download(name: str) -> FileResponse:
    file = mc.fget_object(MINIO_BUCKET, name, name)
    return FileResponse(file._object_name)


@router.get("/list", name="files:list")
async def list_objects():
    return mc.list_objects("bucket")


@router.post("", name="files:create")
async def create(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        results.append(mc.fput_object(MINIO_BUCKET, file.filename, file.file.fileno()))
    return results


@router.delete("", name="files:delete")
async def delete(name: str):
    return mc.remove_object(MINIO_BUCKET, name)
