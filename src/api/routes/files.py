from fastapi import APIRouter, UploadFile, File
from minio import Minio
from typing import List
import os

router = APIRouter()
BUCKET = os.getenv("MINIO_BUCKET_NAME") or "bucket"
mc = Minio(
  os.getenv("MINIO_URL") or "localhost:9000", 
  os.getenv("MINIO_ACCESS_KEY") or "minio", 
  os.getenv("MINIO_SECRET_KEY") or "minio123",
  secure=False
)

if not mc.bucket_exists(BUCKET):
  mc.make_bucket(BUCKET)


@router.get("", name="files:list")
async def list():
  return mc.list_objects("bucket")

@router.post("", name="files:create")
async def create(files: List[UploadFile] = File(...)):
  results = []
  for file in files:
    results.append(mc.fput_object(BUCKET, file.filename, file.file.fileno()))
  return results
