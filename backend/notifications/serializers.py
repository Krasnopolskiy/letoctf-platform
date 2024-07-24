from rest_framework import serializers

from backend.notifications.models import Notification
from backend.storage.serializers import S3FileSerializer
from backend.user.models import User


class NotificationSerializer(serializers.ModelSerializer):
    files = S3FileSerializer(many=True, read_only=True)

    class Meta:
        model = Notification
        fields = (
            "id",
            "created_at",
            "title",
            "description",
            "type",
            "files",
        )


class NotificationRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
