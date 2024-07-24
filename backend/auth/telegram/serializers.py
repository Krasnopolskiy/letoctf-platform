from rest_framework import serializers

from backend.auth.telegram.models import Telegram
from backend.user.models import User


class TelegramLinkStaffSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="invite")

    class Meta:
        model = Telegram
        fields = (
            "user",
            "tg_id",
            "first_name",
            "last_name",
            "username",
        )
