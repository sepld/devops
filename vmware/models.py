from django.db import models
from api.vmomi import VimAPI


# # Create your models here.
class Vcenter(models.Model):
    user = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)
    port = models.CharField(max_length=20, default=443)
    host = models.GenericIPAddressField()

    def vimapi(self):
        """
        获取pyvmomi api对象
        :return:
        """
        vimapi = VimAPI(self.host, self.user, self.pwd, self.port)
        return vimapi


class ObjectVM(models.Model):
    name = models.CharField(max_length=255)
    moid = models.CharField(max_length=30)
    vcenter = models.ForeignKey(Vcenter, null=True, on_delete=models.SET_NULL)


class ComputeResource(ObjectVM):
    is_cluster = models.BooleanField()
    ha = models.NullBooleanField()
    drs = models.NullBooleanField()


class ResourcePool(ObjectVM):
    owner = models.ForeignKey(ComputeResource, null=True, on_delete=models.SET_NULL)


class Datastore(ObjectVM):
    type = models.CharField(max_length=20)
    url = models.CharField(max_length=200)


class Network(ObjectVM):
    net = models.GenericIPAddressField(protocol='ipv4')
    netmask = models.PositiveSmallIntegerField(default=24)
    accessible = models.BooleanField(default=True)


class HostSystem(ObjectVM):
    network = models.ManyToManyField(Network)
    datastore = models.ManyToManyField(Datastore)
    cluster = models.ForeignKey(ComputeResource, null=True, on_delete=models.SET_NULL)


class VirtualMachine(models.Model):
    datastore = models.ManyToManyField(Datastore)
    hostsystem = models.ForeignKey(HostSystem, null=True, on_delete=models.SET_NULL)
    network = models.ManyToManyField(Network)
    resourcepool = models.ForeignKey(ResourcePool, null=True, on_delete=models.SET_NULL)


class IpUsage(models.Model):
    network = models.ForeignKey(Network, null=True, on_delete=models.SET_NULL)
    ipaddress = models.GenericIPAddressField()
    virtualmachine = models.ForeignKey(VirtualMachine, null=True, on_delete=models.SET_NULL)
