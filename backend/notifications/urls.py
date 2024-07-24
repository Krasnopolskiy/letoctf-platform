from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.notifications.views import NotificationRecipientsView, NotificationsStaffViewSet, NotificationsViewSet

router = DefaultRouter()
router.register(r"notifications", NotificationsViewSet, basename="notifications")
router.register(r"staff/notifications", NotificationsStaffViewSet, basename="notifications_staff")

urlpatterns = [
    path(
        "staff/notifications/<int:notification_id>/recipients/",
        NotificationRecipientsView.as_view(),
        name="notification_recipients",
    ),
]
urlpatterns += router.urls
