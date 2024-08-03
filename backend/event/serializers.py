from rest_framework import serializers

from backend.event.models import Event, Feedback
from backend.storage.serializers import S3FileSerializer
from backend.user.models import User


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


class FeedbackSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Feedback
        fields = (
            "score",
            "text",
            "event",
            "user",
        )
