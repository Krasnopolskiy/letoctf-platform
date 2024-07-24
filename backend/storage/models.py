import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from backend.storage.client import get_s3_client


class S3File(models.Model):
    file = models.FileField(upload_to="uploads/")
    s3_key = models.CharField(max_length=255, unique=True, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.s3_key:
            self.s3_key = f"{uuid.uuid4()}/{self.file.name}"

        super().save(*args, **kwargs)
        s3_client = get_s3_client()
        s3_client.upload_fileobj(self.file, settings.MINIO_BUCKET_NAME, self.s3_key)

    def delete(self, *args, **kwargs):
        s3_client = get_s3_client()
        s3_client.delete_object(Bucket=settings.MINIO_BUCKET_NAME, Key=self.s3_key)

        super().delete(*args, **kwargs)

    @property
    def url(self) -> str:
        return f"{settings.MINIO_HOST}/{settings.MINIO_BUCKET_NAME}/{self.s3_key}"

    @property
    def signed_url(self) -> str:
        s3_client = get_s3_client()
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.MINIO_BUCKET_NAME, "Key": self.s3_key},
            ExpiresIn=3600,
        )

    def __str__(self) -> str:
        return f"File for {self.content_object}"
