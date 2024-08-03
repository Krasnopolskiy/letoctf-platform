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
    type = models.PositiveSmallIntegerField(
        choices=Type.choices, default=Type.ALL, help_text="Who can see the notification"
    )

    active = models.BooleanField(default=True, help_text="When set to false, the notification is hidden fr")
    start = models.DateTimeField(null=True, blank=True, help_text="If set, notification is hidden before this time")
    end = models.DateTimeField(null=True, blank=True, help_text="If set, notification is hidden after this time")

    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        help_text="Notification recipient",
    )
    team = models.ForeignKey(
        "user.Team",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        help_text="Notification recipient",
    )
    files = GenericRelation("storage.S3File", help_text="Notification files")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
