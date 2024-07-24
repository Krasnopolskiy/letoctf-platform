from django.contrib import admin
from django.urls import include, path

api_urlpatterns = [
    path("", include("backend.auth.urls")),
    path("", include("backend.user.urls")),
    path("", include("backend.challenge.urls")),
    path("", include("backend.event.urls")),
    path("", include("backend.statistics.urls")),
    path("", include("backend.notifications.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns)),
]
