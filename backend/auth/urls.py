from django.urls import include, path

urlpatterns = [
    path("auth/token/", include("backend.auth.jwt.urls")),
    path("auth/telegram/", include("backend.auth.telegram.urls")),
]
