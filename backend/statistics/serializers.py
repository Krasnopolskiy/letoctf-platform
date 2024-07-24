from rest_framework import serializers

from backend.user.models import User
from backend.user.serializers import TeamSerializer


class StatisticsSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=False, read_only=True)

    personal_score = serializers.FloatField()
    team_score = serializers.FloatField()
    score = serializers.FloatField()

    team_place = serializers.IntegerField()
    place = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            "id",
            "is_staff",
            "username",
            "team",
            "personal_score",
            "team_score",
            "score",
            "team_place",
            "place",
        )
