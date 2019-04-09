from scripts.models import Scripts
from scripts.serializers import ScriptsSerializers
from rest_framework import viewsets
from rest_framework import permissions


# Create your views here.

class ScriptsViewSet(viewsets.ModelViewSet):
    queryset = Scripts.objects.all()
    serializer_class = ScriptsSerializers
    permission_classes = (permissions.IsAuthenticated,)


