from rest_framework import serializers

from backend.challenge.models import Challenge
from backend.storage.serializers import S3FileSerializer
from backend.user.models import Team, User
from backend.user.serializers import UserSerializer


class ChallengeSerializer(serializers.ModelSerializer):
    solved = serializers.BooleanField(read_only=True)
    files = S3FileSerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        fields = (
            "id",
            "name",
            "description",
            "score",
            "team",
            "review",
            "hidden",
            "start",
            "end",
            "solved",
            "files",
        )


class SubmitStaffSerializer(serializers.Serializer):
    flag = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class UserScoreSerializer(serializers.ModelSerializer):
    score = serializers.FloatField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "score",
        )


class TeamScoreSerializer(serializers.ModelSerializer):
    score = serializers.FloatField()
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "score",
            "users",
        )
