from user.serializers import UserSerializers
from user.models import User
from rest_framework import viewsets
from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (permissions.IsAuthenticated,)
