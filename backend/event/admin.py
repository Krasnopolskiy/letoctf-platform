from django.contrib import admin
from django.contrib.admin import register

from backend.event.models import Event
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

    description_info.short_description = "Description"
