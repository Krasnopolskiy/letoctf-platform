from __future__ import annotations

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Notification(models.Model):
    class Type(models.IntegerChoices):
        PERSONAL = 0, "Personal"
        TEAM = 1, "Team"
        ALL = 2, "All"

    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=Type.choices, default=Type.ALL)

    active = models.BooleanField(default=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
    team = models.ForeignKey("user.Team", on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
    files = GenericRelation("storage.S3File")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
