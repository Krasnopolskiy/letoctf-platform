import uuid
from secrets import token_hex

from coolname import generate_slug
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Case, Count, F, Max, OuterRef, QuerySet, Subquery, Sum, When
from django.db.models.functions import Coalesce, Greatest

from backend.challenge.models import Submission


def get_coolname() -> str:
    return generate_slug(3)


def get_password() -> str:
    return token_hex(16)


class CustomUserManager(UserManager):
    def annotate_score(self) -> QuerySet:
        user_submission_subquery = (
            Submission.objects.select_related("challenge")
            .filter(challenge__active=True, correct=True, challenge__team=False, user_id=OuterRef("pk"))
            .values("user_id")
            .annotate(total_score=Sum("challenge__score"), last_user_submission=Max("created_at"))
            .values("total_score", "last_user_submission")
        )

        team_submission_subquery = (
            Submission.objects.select_related("challenge")
            .filter(challenge__active=True, correct=True, challenge__team=True, team_id=OuterRef("team__id"))
            .values("team_id")
            .annotate(total_score=Sum("challenge__score"), last_team_submission=Max("created_at"))
            .values("total_score", "last_team_submission")
        )

        team_count_subquery = Team.objects.filter(id=OuterRef("team__id")).annotate(size=Count("users")).values("size")

        return self.select_related("team").annotate(
            personal_score=Coalesce(Subquery(user_submission_subquery.values("total_score")), 0),
            last_user_submission=Subquery(user_submission_subquery.values("last_user_submission")),
            team_score=Coalesce(Subquery(team_submission_subquery.values("total_score")), 0),
            last_team_submission=Subquery(team_submission_subquery.values("last_team_submission")),
            team_size=Coalesce(Subquery(team_count_subquery), 1),
            score=Case(
                When(team__isnull=False, then=F("personal_score") + F("team_score") / F("team_size")),
                default=F("personal_score"),
            ),
            last_submission=Greatest(
                F("last_user_submission"), F("last_team_submission"), output_field=models.DateTimeField()
            ),
        )


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, help_text="Username, by default 'Last name First name'")
    password = models.CharField(max_length=128, default=get_password, help_text="User password")

    student = models.BooleanField(default=True, help_text="Whether or not the user is a student")
    invite = models.CharField(max_length=36, default=uuid.uuid4, help_text="User invite code")
    team = models.ForeignKey(
        "Team", on_delete=models.SET_NULL, null=True, blank=True, related_name="users", help_text="User's team"
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text="User creation date")

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username


class TeamManager(models.Manager):
    def annotate_score(self) -> QuerySet:
        team_submissions_query = (
            Submission.objects.select_related("challenge")
            .filter(challenge__active=True, correct=True, challenge__team=True, team_id=OuterRef("pk"))
            .values("team_id")
            .annotate(total_score=Sum("challenge__score"), last_team_submission=Max("created_at"))
            .values("total_score", "last_team_submission")
        )

        return self.prefetch_related("users").annotate(
            score=Coalesce(Subquery(team_submissions_query.values("total_score")), 0),
            last_submission=Subquery(team_submissions_query.values("last_team_submission")),
        )


class Team(models.Model):
    name = models.CharField(max_length=250, default=get_coolname, help_text="Team name")
    invite = models.CharField(max_length=36, default=uuid.uuid4, help_text="Team invite code")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Team creation date")

    objects = TeamManager()

    def __str__(self) -> str:
        return self.name
