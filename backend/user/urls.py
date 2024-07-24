from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.user.views import JoinTeamView, TeamViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"teams", TeamViewSet, basename="teams")

urlpatterns = [
    path("teams/join/", JoinTeamView.as_view(), name="join_team"),
]
urlpatterns += router.urls
