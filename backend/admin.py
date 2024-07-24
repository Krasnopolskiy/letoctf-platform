from typing import Any, Type

from django.db.models import Model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString


def get_admin_url(model: Type[Model] | Model, page_code: str = "change", *args, **kwargs) -> str:
    url_name = f"admin:{model._meta.app_label}_{model._meta.model_name}_{page_code}"
    return reverse(url_name, *args, **kwargs)


def view_link(url: str, body: Any, new_window: bool = False) -> SafeString:
    target = ' target="_blank"' if new_window else ""
    return format_html('<a class="viewlink" href="{}"{}>{}</a>', url, target, str(body))


def get_change_link(obj: Type[Model] | Model | None, title: str | None = None) -> str | SafeString:
    if not obj:
        return "-"
    title = title or str(obj)
    return view_link(get_admin_url(obj, "change", args=(obj.pk,)), title)
