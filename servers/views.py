from servers.models import Servers
from servers.serializers import ServersSerializers
from rest_framework import viewsets
from rest_framework import permissions

# Create your views here.

class ServersViewSet(viewsets.ModelViewSet):
    queryset = Servers.objects.all()
    serializer_class = ServersSerializers
    permission_classes = (permissions.IsAuthenticated,)
