from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    speaker = models.CharField(max_length=250, null=True, blank=True)
    affiliation = models.CharField(max_length=250, null=True, blank=True)

    start = models.DateTimeField()
    end = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    files = GenericRelation("storage.S3File")

    def __str__(self) -> str:
        return self.title


class Feedback(models.Model):
    score = models.IntegerField(help_text="Score from 1 to 5")
    text = models.TextField()
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="feedbacks", help_text="User who made the feedback"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="feedbacks")

    def __str__(self) -> str:
        return self.text
