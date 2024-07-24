from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.notifications.models import Notification
from backend.notifications.serializers import NotificationRecipientSerializer, NotificationSerializer
from backend.user.models import User


class NotificationsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.filter(active=True).order_by("-created_at")

    def apply_filter(self, user_id: int | None = None, team_id: int | None = None) -> QuerySet[Notification]:
        now = timezone.localtime(timezone.now())
        return self.queryset.filter(
            Q(start__lte=now) | Q(start=None),
            Q(end__gte=now) | Q(end=None),
        ).filter(
            Q(type=Notification.Type.PERSONAL, user_id=user_id)
            | Q(type=Notification.Type.TEAM, team_id=team_id)
            | Q(type=Notification.Type.ALL),
        )

    def get_queryset(self) -> QuerySet[Notification]:
        user_id = self.request.query_params.get("user_id", None)
        if user := User.objects.filter(pk=user_id).first():
            team_id = user.team_id
        else:
            user_id, team_id = None, None
        return self.apply_filter(user_id, team_id)


class NotificationsStaffViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.filter(active=True).order_by("-created_at")
    permission_classes = (IsAdminUser,)

    def get_queryset(self) -> QuerySet[Notification]:
        now = timezone.localtime(timezone.now())
        return self.queryset.filter(
            Q(start__lte=now) | Q(start=None),
            Q(end__gte=now) | Q(end=None),
        )


class NotificationRecipientsView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, notification_id: int, *args, **kwargs):
        notification = get_object_or_404(Notification, pk=notification_id)
        if notification.type == Notification.Type.PERSONAL:
            users = User.objects.filter(id=notification.user_id)
        elif notification.type == Notification.Type.TEAM:
            users = User.objects.filter(team=notification.team)
        else:
            users = User.objects.all()
        return Response(NotificationRecipientSerializer(users, many=True).data)
