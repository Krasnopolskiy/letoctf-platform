from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.statistics.views import StatisticsView

router = DefaultRouter()

urlpatterns = [
    path("statistics/<int:user_id>/", StatisticsView.as_view(), name="statistics"),
]
