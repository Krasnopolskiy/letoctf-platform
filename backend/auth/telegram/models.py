from django.db import models

from backend.user.models import User


class Telegram(models.Model):
    tg_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="telegram")

    def __str__(self) -> str:
        return f"{self.username} [{self.tg_id}]"
