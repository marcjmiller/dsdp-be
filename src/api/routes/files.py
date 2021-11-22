from fastapi import APIRouter
from minio import Minio
import os

router = APIRouter()

minio_client = Minio(
  os.getenv("MINIO_URL"), 
  os.getenv("MINIO_ACCESS_KEY"), 
  os.getenv("MINIO_SECRET_KEY"),
  secure=False
)


@router.get("", name="files:list")
async def list():
  return minio_client.list_buckets()
