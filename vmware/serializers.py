from rest_framework import serializers
from vmware.models import Vcenter


class VcenterSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vcenter
        fields = ('url', 'id', 'host', 'user', 'pwd', 'port')

