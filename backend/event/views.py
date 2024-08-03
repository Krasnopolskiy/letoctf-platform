from django.db.models import QuerySet
from django.utils import timezone
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet

from backend.event.models import Event
from backend.event.serializers import EventSerializer, FeedbackSerializer


class EventViewSet(ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_queryset(self) -> QuerySet[Event]:
        start_of_day = timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timezone.timedelta(days=1)
        return self.queryset.filter(start__gte=start_of_day, start__lt=end_of_day).order_by("start")


class FeedbackCreateView(CreateAPIView):
    permission_classes = (IsAdminUser,)

    serializer_class = FeedbackSerializer
    queryset = Event.objects.all()
