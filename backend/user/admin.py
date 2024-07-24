from admin_searchable_dropdown.filters import AutocompleteFilterFactory
from django import forms
from django.contrib import admin
from django.contrib.admin import register
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.db.models import Q
from django.utils.html import format_html

from backend.admin import get_change_link
from backend.user.models import Team, User


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "team_info",
        "invite",
        "is_staff",
        "student",
    )
    list_filter = (
        AutocompleteFilterFactory("Team", "team"),
        "is_staff",
        "student",
    )

    search_fields = ("username", "invite")
    readonly_fields = ("id", "created_at")
    autocomplete_fields = ("team",)

    ordering = ("username",)

    def team_info(self, obj: User) -> str:
        return get_change_link(obj.team)

    team_info.short_description = "Team"


class TeamAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Users", is_stacked=False),
    )

    class Meta:
        model = Team
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.users.all()

    def save(self, commit: bool = True):
        team = super().save(commit=False)
        if commit:
            team.save()
        if team.pk:
            team.users.set(self.cleaned_data["users"])
        return team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    form = TeamAdminForm

    list_display = ("name", "invite", "user_list")

    search_fields = ("name",)
    readonly_fields = ("id", "created_at")

    ordering = ("name",)

    def get_form(self, request: WSGIRequest, obj: Team | None = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["users"].queryset = User.objects.filter(
                Q(team=obj) | Q(team__isnull=True),
            )
        return form

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        selected_users = form.cleaned_data.get("users")
        if selected_users is not None:
            current_users = set(obj.users.all())
            selected_users_set = set(selected_users)

            users_to_add = selected_users_set - current_users
            for user in users_to_add:
                user.team = obj

            users_to_remove = current_users - selected_users_set
            for user in users_to_remove:
                user.team = None

            User.objects.bulk_update(users_to_add, ["team"])
            User.objects.bulk_update(users_to_remove, ["team"])

    def user_list(self, obj):
        users = [get_change_link(user) for user in obj.users.all()]
        return format_html("<br/>".join(users))

    user_list.short_description = "Users"
