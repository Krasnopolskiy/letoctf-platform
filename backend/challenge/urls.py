from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.challenge.views import (
    ChallengeViewSet,
    SubmitChallengeStaffView,
    SubmitHiddenChallengeStaffView,
    TeamScoreboardView,
    UserScoreboardView,
)

router = DefaultRouter()
router.register(r"challenges", ChallengeViewSet, basename="challenges")

urlpatterns = [
    path("scoreboard/users/", UserScoreboardView.as_view(), name="user_scoreboard"),
    path("scoreboard/teams/", TeamScoreboardView.as_view(), name="team_scoreboard"),
    path("challenges/<int:pk>/submit/staff/", SubmitChallengeStaffView.as_view(), name="submit_challenge"),
    path("challenges/submit/staff/", SubmitHiddenChallengeStaffView.as_view(), name="submit_hidden_challenge"),
]

urlpatterns += router.urls
