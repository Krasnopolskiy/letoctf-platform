from admin_searchable_dropdown.filters import AutocompleteFilterFactory
from django.contrib import admin

from backend.admin import get_change_link, view_link
from backend.auth.telegram.models import Telegram


@admin.register(Telegram)
class TelegramAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user_info",
        "telegram_link",
        "tg_id",
    )
    list_filter = (AutocompleteFilterFactory("User", "user"),)

    search_fields = (
        "tg_id",
        "username",
        "first_name",
        "last_name",
        "user__username",
    )
    readonly_fields = ("id", "created_at")
    autocomplete_fields = ("user",)

    ordering = ("-user",)

    def user_info(self, obj: Telegram) -> str:
        return get_change_link(obj.user)

    def telegram_link(self, obj: Telegram) -> str:
        link = f"https://t.me/{obj.username}"
        return view_link(link, "Contact")
