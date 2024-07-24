from django.db.models import F, QuerySet, Window
from django.db.models.functions import RowNumber
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.statistics.serializers import StatisticsSerializer
from backend.user.models import Team, User


class StatisticsView(APIView):
    queryset = User.objects.annotate_score()
    serializer_class = StatisticsSerializer

    def get_user_place(self, queryset: QuerySet[User], user_id: int) -> int:
        values = queryset.annotate(
            place=Window(
                expression=RowNumber(),
                order_by=[F("score").desc(), F("last_user_submission").asc(), F("last_team_submission").asc()],
            ),
        ).values_list("pk", "place")
        return next(place for (pk, place) in values if pk == user_id)

    def get_team_place(self, queryset: QuerySet[Team], team_id: int) -> int:
        values = queryset.annotate(
            place=Window(expression=RowNumber(), order_by=[F("score").desc(), F("last_submission").asc()]),
        ).values_list("pk", "place")
        return next(place for (pk, place) in values if pk == team_id)

    def get(self, request, user_id: int, *args, **kwargs):
        user = get_object_or_404(self.queryset, pk=user_id)
        user.place = self.get_user_place(self.queryset, user_id)
        if user.team_id:
            user.team_place = self.get_team_place(Team.objects.annotate_score(), user.team_id)
        else:
            user.team_place = None

        return Response(StatisticsSerializer(user).data)
