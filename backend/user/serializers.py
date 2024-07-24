from rest_framework import serializers

from backend.user.models import Team, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )


class TeamSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "users",
        )


class JoinTeamSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    invite = serializers.UUIDField()

    class Meta:
        fields = (
            "user",
            "invite",
        )
