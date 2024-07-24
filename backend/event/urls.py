from rest_framework.routers import DefaultRouter

from backend.event.views import EventViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="events")

urlpatterns = router.urls
