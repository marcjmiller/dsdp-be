import boto3
from typing import Generator

from app.core.config import get_settings

settings = get_settings()


def get_s3_client() -> Generator:
    print(f"temp url log*** {settings.MINIO_ENDPOINT_URL}")
    client = boto3.client(
        "s3",
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        endpoint_url=settings.MINIO_ENDPOINT_URL,
    )
    yield client
