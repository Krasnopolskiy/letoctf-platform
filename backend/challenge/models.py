from __future__ import annotations

import re

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Exists, OuterRef


class ChallengeQuerySet(models.QuerySet):
    def annotate_solved(self, user_id: int | None = None, team_id: int | None = None) -> models.QuerySet[Challenge]:
        solved_by_user = Submission.objects.filter(challenge=OuterRef("pk"), user_id=user_id, correct=True)
        solved_by_team = Submission.objects.filter(
            challenge=OuterRef("pk"), challenge__team=True, team_id=team_id, correct=True
        )
        return self.annotate(solved=Exists(solved_by_user) | Exists(solved_by_team))


class Challenge(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    score = models.IntegerField()
    flag = models.CharField(max_length=250, null=True, blank=True)

    active = models.BooleanField(default=True, help_text="When set to false, the challenge is hidden")
    team = models.BooleanField(default=False, help_text="Whether or not the challenge is a team challenge")
    hidden = models.BooleanField(
        default=False, help_text="When set to true, the challenge is not visible, but it can still be submitted"
    )
    review = models.BooleanField(
        default=False, help_text="Whether or not the challenge requires review from the admins team"
    )
    regexp = models.BooleanField(default=False, help_text="Whether or not the flag is a regular expression")

    start = models.DateTimeField(null=True, blank=True, help_text="If set, challenge is hidden before this time")
    end = models.DateTimeField(null=True, blank=True, help_text="If set, challenge is hidden after this time")

    created_at = models.DateTimeField(auto_now_add=True)

    files = GenericRelation("storage.S3File")

    objects = ChallengeQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name

    def submit(self, flag: str, user_id: int, team_id: int | None = None) -> bool:
        if self.review:
            return False

        if self.regexp:
            correct = re.match(self.flag, flag) is not None
        else:
            correct = self.flag.lower() == flag.lower()

        if self.team:
            if not team_id:
                return False

            if Submission.objects.filter(challenge=self, team_id=team_id, correct=True).exists():
                return correct

        params = {
            "challenge_id": self.id,
            "correct": correct,
            "flag": flag,
            "user_id": user_id,
        }

        if self.team:
            params["team_id"] = team_id

        Submission.objects.get_or_create(**params)

        return correct


class Submission(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="submissions")
    correct = models.BooleanField(default=True)
    flag = models.CharField(max_length=250, null=True, blank=True)

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="submissions")
    team = models.ForeignKey("user.Team", on_delete=models.CASCADE, null=True, blank=True, related_name="submissions")

    created_at = models.DateTimeField(auto_now_add=True)

    files = GenericRelation("storage.S3File")

    def __str__(self) -> str:
        return f"Challenge #{self.challenge_id} submission"
