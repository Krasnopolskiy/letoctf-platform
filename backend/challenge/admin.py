from admin_searchable_dropdown.filters import AutocompleteFilterFactory
from django.contrib import admin
from django.contrib.admin import register
from django.utils.html import format_html

from backend.admin import get_change_link
from backend.challenge.models import Challenge, Submission
from backend.storage.admin import S3FileInline


@register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description_info",
        "score",
        "submits",
        "files",
        "start",
        "end",
        "active",
        "hidden",
        "team",
    )
    list_filter = (
        "start",
        "end",
        "team",
        "active",
        "hidden",
    )

    search_fields = ("name", "description", "flag")
    readonly_fields = ("id", "created_at")

    ordering = ("-start", "end", "name")

    inlines = [S3FileInline]

    def description_info(self, obj: Challenge) -> str:
        description = obj.description or "-"
        return description[:100] + ("..." if len(description) > 100 else "")

    def files(self, obj: Challenge) -> str:
        files = [get_change_link(file, file.file) for file in obj.files.all()]
        return format_html("<br/>".join(files))

    def submits(self, obj: Challenge) -> int:
        return obj.submissions.count()

    description_info.short_description = "Description"


@register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "challenge_info",
        "user_info",
        "team_info",
        "flag",
        "correct",
        "created_at",
    )
    list_filter = (
        AutocompleteFilterFactory("Challenge", "challenge"),
        AutocompleteFilterFactory("User", "user"),
        AutocompleteFilterFactory("Team", "team"),
        "correct",
        "created_at",
    )

    search_fields = (
        "challenge__name",
        "user__username",
        "team__name",
        "flag",
    )
    readonly_fields = ("id", "created_at")
    autocomplete_fields = ("challenge", "user", "team")

    ordering = ("-created_at",)

    def challenge_info(self, obj: Submission) -> str:
        return get_change_link(obj.challenge)

    def user_info(self, obj: Submission) -> str:
        return get_change_link(obj.user)

    def team_info(self, obj: Submission) -> str:
        return get_change_link(obj.team)

    challenge_info.short_description = "Challenge"
    user_info.short_description = "User"
    team_info.short_description = "Team"
