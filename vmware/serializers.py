from rest_framework import serializers
from vmware.models import Vcenter, VirtualMachine


class VcenterSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vcenter
        fields = ('url', 'id', 'host', 'user', 'pwd', 'port')


class VirtualMachineSerializers(serializers.HyperlinkedModelSerializer):
    ipaddress = serializers.IPAddressField(source='IpUsage.ipaddress')

    class Meta:
        model = VirtualMachine
        fields = ('url', 'id', 'datastore', 'hostsystem', 'network', 'resourcepool', 'ipaddress')
