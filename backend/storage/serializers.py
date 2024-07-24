from rest_framework import serializers

from backend.storage.models import S3File


class S3FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = S3File
        fields = (
            "id",
            "s3_key",
        )
