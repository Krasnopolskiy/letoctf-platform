from admin_searchable_dropdown.filters import AutocompleteFilterFactory
from django.contrib import admin
from django.utils.html import format_html

from backend.admin import get_change_link
from backend.notifications.models import Notification
from backend.storage.admin import S3FileInline


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description_info",
        "type",
        "user_info",
        "team_info",
        "start",
        "end",
        "active",
    )
    list_filter = (
        AutocompleteFilterFactory("User", "user"),
        AutocompleteFilterFactory("Team", "team"),
        "start",
        "end",
        "active",
    )

    search_fields = ("title", "description")
    readonly_fields = ("id", "created_at")
    autocomplete_fields = ("user", "team")

    inlines = [S3FileInline]

    def description_info(self, obj: Notification) -> str:
        description = obj.description or "-"
        return description[:100] + ("..." if len(description) > 100 else "")

    def files(self, obj: Notification) -> str:
        files = [get_change_link(file, file.file) for file in obj.files.all()]
        return format_html("<br/>".join(files))

    def user_info(self, obj: Notification) -> str:
        return get_change_link(obj.user)

    def team_info(self, obj: Notification) -> str:
        return get_change_link(obj.team)

    description_info.short_description = "Description"
    user_info.short_description = "User"
    team_info.short_description = "Team"
