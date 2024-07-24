from rest_framework import serializers

from backend.event.models import Event
from backend.storage.serializers import S3FileSerializer


class EventSerializer(serializers.ModelSerializer):
    files = S3FileSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "speaker",
            "affiliation",
            "start",
            "end",
            "files",
        )
