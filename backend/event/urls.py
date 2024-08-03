from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.event.views import EventViewSet, FeedbackCreateView

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="events")

urlpatterns = [
    path("events/<int:pk>/feedback/", FeedbackCreateView.as_view(), name="event_feedback"),
]
urlpatterns += router.urls
