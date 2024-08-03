from django.contrib import admin
from django.contrib.admin import register
from django.db.models import Avg

from backend.admin import get_change_link
from backend.event.models import Event, Feedback
from backend.storage.admin import S3FileInline


@register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description_info",
        "start",
        "end",
        "speaker",
        "affiliation",
        "mean_score",
    )
    list_filter = (
        "speaker",
        "affiliation",
        "start",
        "end",
    )

    search_fields = (
        "title",
        "description",
        "speaker",
        "affiliation",
    )
    readonly_fields = ("id", "created_at")

    ordering = ("-start",)

    inlines = [S3FileInline]

    def description_info(self, obj: Event) -> str:
        description = obj.description or "-"
        return description[:100] + ("..." if len(description) > 100 else "")

    def mean_score(self, obj: Event) -> str:
        mean_score = obj.feedbacks.aggregate(Avg("score"))["score__avg"]
        return f"{mean_score:.2f}" if mean_score else "-"

    description_info.short_description = "Description"


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "event_link",
        "score",
        "text",
    )
    list_filter = (
        "event",
        "score",
    )

    search_fields = (
        "event",
        "text",
    )

    def event_link(self, obj: Feedback) -> str:
        return get_change_link(obj.event)

    event_link.short_description = "Event"
