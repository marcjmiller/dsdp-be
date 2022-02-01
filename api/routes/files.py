import os
import logging
from typing import List
from fastapi import APIRouter, UploadFile, File
from minio import Minio
from starlette.responses import FileResponse

files_router = APIRouter()

MINIO_BUCKET = os.getenv("MINIO_BUCKET_NAME", "bucket")
MINIO_HOST = os.getenv("MINIO_HOST", "localhost")
MINIO_PORT = os.getenv("MINIO_PORT", "9000")
MINIO_PROTOCOL = os.getenv("MINIO_PROTOCOL", "http")
MINIO_URL = f"{MINIO_HOST}:{MINIO_PORT}"
MINIO_REGION = os.getenv("MINIO_REGION")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio123")

mc = Minio(
    MINIO_URL,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    region=MINIO_REGION,
    secure=MINIO_PROTOCOL == "https",
)

if not mc.bucket_exists(MINIO_BUCKET):
    mc.make_bucket(MINIO_BUCKET)

@files_router.get("", name="files:getFile", response_class=FileResponse)
async def download(name: str) -> FileResponse:
    return mc.fget_object(MINIO_BUCKET, name, name)._object_name


@files_router.get("/list", name="files:list")
async def list_objects():
    return mc.list_objects(MINIO_BUCKET)


@files_router.post("", name="files:create")
async def create(files: List[UploadFile] = File(...)):
    logging.info("backend log")
    return mc.fput_object(MINIO_BUCKET, files[0].filename, files[0].file.fileno())


@files_router.delete("", name="files:delete")
async def delete(name: str):
    return mc.remove_object(MINIO_BUCKET, name)
