from rest_framework import serializers
from servers.models import Servers


class ServersSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Servers
        fields = ('url', 'id', 'ip')
