from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from backend.admin import get_change_link, view_link
from backend.storage.models import S3File


@admin.register(S3File)
class S3FileAdmin(admin.ModelAdmin):
    pass
    list_display = (
        "__str__",
        "content_object_info",
        "file_link",
        "created_at",
    )
    list_filter = ("content_type", "created_at")

    search_fields = ("s3_key",)
    readonly_fields = (
        "file_link",
        "content_object_info",
        "s3_key",
        "created_at",
    )

    def file_link(self, obj: S3File) -> str:
        if not obj.pk:
            return "File not yet uploaded"
        return view_link(obj.url, "Download")

    def content_object_info(self, obj: S3File) -> str:
        return get_change_link(obj.content_object) if obj.pk else "-"

    file_link.short_description = "File Link"
    content_object_info.short_description = "Content Object"


class S3FileInline(GenericTabularInline):
    model = S3File
    extra = 0
    fields = ("file", "file_link")
    readonly_fields = ("file_link",)

    def file_link(self, obj: S3File) -> str:
        if not obj.pk:
            return "File not yet uploaded"
        return view_link(obj.url, "Download")
