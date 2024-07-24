from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.user.models import Team, User
from backend.user.serializers import JoinTeamSerializer, TeamSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class JoinTeamView(APIView):
    serializer_class = JoinTeamSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = JoinTeamSerializer(data=request.data)
        if not data.is_valid():
            return Response(data.errors, status=400)

        user = data.validated_data["user"]
        invite = data.validated_data["invite"]

        team = get_object_or_404(Team, invite=invite)
        user.team = team
        user.save(update_fields=["team"])

        return Response({"success": True})
