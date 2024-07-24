from boto3 import Session
from botocore.client import BaseClient
from django.conf import settings


def get_s3_client() -> BaseClient:
    return Session(
        region_name=settings.MINIO_REGION,
    ).client(
        service_name="s3",
        endpoint_url=settings.MINIO_HOST,
        aws_access_key_id=settings.MINIO_ROOT_USER,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
    )
