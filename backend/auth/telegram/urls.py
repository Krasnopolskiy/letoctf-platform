from django.urls import path

from backend.auth.telegram.views import FindUserByTelegramView, TelegramLinkStaffView

urlpatterns = [
    path("staff/", TelegramLinkStaffView.as_view(), name="staff_telegram_link"),
    path("<str:tg_id>/", FindUserByTelegramView.as_view(), name="find_user_by_telegram"),
]
