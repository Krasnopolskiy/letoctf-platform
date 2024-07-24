from django.http import Http404
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication

from backend.auth.telegram.models import Telegram
from backend.auth.telegram.serializers import TelegramLinkStaffSerializer
from backend.user.models import User
from backend.user.serializers import UserSerializer


class TelegramLinkStaffView(CreateAPIView):
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = TelegramLinkStaffSerializer
    queryset = Telegram.objects.all()


class FindUserByTelegramView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        tg_id = self.kwargs.get("tg_id")
        try:
            user = self.queryset.get(telegram__tg_id=tg_id)
        except User.DoesNotExist:
            raise Http404("User not found")
        return Response(UserSerializer(user).data)
