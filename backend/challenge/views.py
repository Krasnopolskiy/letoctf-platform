from django.db.models import Q, QuerySet
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication

from backend.challenge.models import Challenge
from backend.challenge.serializers import (
    ChallengeSerializer,
    SubmitStaffSerializer,
    TeamScoreSerializer,
    UserScoreSerializer,
)
from backend.user.models import Team, User


class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChallengeSerializer
    queryset = Challenge.objects.annotate_solved().filter(active=True, dynamic=False)

    def apply_filter(self, queryset: QuerySet[Challenge]) -> QuerySet[Challenge]:
        now = timezone.localtime(timezone.now())
        return queryset.filter(
            Q(
                Q(hidden=False),
                Q(start__lte=now) | Q(start=None),
                Q(end__gte=now) | Q(end=None),
            )
            | Q(solved=True),
        )

    def get_queryset(self) -> QuerySet[Challenge]:
        user_id = self.request.query_params.get("user_id", None)
        queryset = self.queryset
        if user := User.objects.filter(id=user_id).first():
            queryset = queryset.annotate_solved(user.id, user.team_id)
        return self.apply_filter(queryset)


class SubmitChallengeStaffView(APIView):
    queryset = Challenge.objects.filter(active=True, dynamic=False, hidden=False)
    serializer_class = SubmitStaffSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self) -> QuerySet[Challenge]:
        now = timezone.localtime(timezone.now())
        return self.queryset.filter(
            Q(start__lte=now) | Q(start=None),
            Q(end__gte=now) | Q(end=None),
        )

    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        challenge = get_object_or_404(self.get_queryset(), pk=pk)
        data = SubmitStaffSerializer(data=request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        flag = data.validated_data["flag"]
        user = data.validated_data["user"]
        correct = challenge.submit(flag, user.id, user.team_id)
        return Response({"correct": correct})


class SubmitHiddenChallengeStaffView(APIView):
    queryset = Challenge.objects.filter(active=True, dynamic=False, hidden=True)
    serializer_class = SubmitStaffSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self) -> QuerySet[Challenge]:
        now = timezone.localtime(timezone.now())
        return self.queryset.filter(
            Q(start__lte=now) | Q(start=None),
            Q(end__gte=now) | Q(end=None),
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = SubmitStaffSerializer(data=request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        flag = data.validated_data["flag"]
        user = data.validated_data["user"]

        challenge = get_object_or_404(self.get_queryset(), flag=flag)
        correct = challenge.submit(flag, user.id, user.team_id)
        return Response({"correct": correct})


class UserScoreboardView(ListAPIView):
    queryset = (
        User.objects.annotate_score()
        .filter(student=True, score__gt=0)
        .order_by("-score", "last_user_submission", "last_team_submission")
    )
    serializer_class = UserScoreSerializer


class TeamScoreboardView(ListAPIView):
    queryset = Team.objects.annotate_score().filter(score__gt=0).order_by("-score", "last_submission")
    serializer_class = TeamScoreSerializer
