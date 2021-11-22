from fastapi import APIRouter
from minio import Minio
import os

router = APIRouter()

client = Minio(os.getenv("MINIO_URL"), os.getenv("MINIO_ACCESS_KEY"), os.getenv("MINIO_SECRET_KEY"))


@router.get("", name="files:list")
async def list():
  return client.list_buckets()
