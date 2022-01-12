import os
from typing import List
from fastapi import APIRouter, UploadFile, File
from minio import Minio
from starlette.responses import FileResponse


router = APIRouter()

BUCKET = os.getenv("MINIO_BUCKET_NAME") or "bucket"
MINIO_HOST = os.getenv("MINIO_HOST") or "localhost"
MINIO_PORT = os.getenv("MINIO_PORT") or "9000"
MINIO_URL = os.getenv("MINIO_URL") or f"{MINIO_HOST}:{MINIO_PORT}"

try:
    mc = Minio(
        MINIO_URL,
        os.getenv("MINIO_ACCESS_KEY") or "minio",
        os.getenv("MINIO_SECRET_KEY") or "minio123",
        secure=False,
    )

    if not mc.bucket_exists(BUCKET):
        mc.make_bucket(BUCKET)
except Exception as exception:
    print(f"Bucket: {BUCKET}, \nMinio_URL: {MINIO_URL}, \nException: {exception}")
    raise exception

@router.get("", name="files:getFile")
async def download(name: str) -> FileResponse:
    file = mc.fget_object(BUCKET, name, name)
    return FileResponse(file._object_name)


@router.get("/list", name="files:list")
async def list_objects():
    return mc.list_objects("bucket")


@router.post("", name="files:create")
async def create(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        results.append(mc.fput_object(BUCKET, file.filename, file.file.fileno()))
    return results


@router.delete("", name="files:delete")
async def delete(name: str):
    return mc.remove_object(BUCKET, name)
