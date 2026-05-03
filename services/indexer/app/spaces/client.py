import boto3
from botocore.client import BaseClient

from app.config import settings


def get_spaces_client() -> BaseClient:
    return boto3.client(
        "s3",
        region_name=settings.DO_SPACES_REGION,
        endpoint_url=settings.DO_SPACES_ENDPOINT,
        aws_access_key_id=settings.DO_SPACES_ACCESS_KEY_ID,
        aws_secret_access_key=settings.DO_SPACES_SECRET_ACCESS_KEY,
    )
