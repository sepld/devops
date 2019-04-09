from vmware.models import *
from vmware.serializers import *
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from api.vmomi import *
from pyVmomi import vim
import itertools


class VcenterViewSet(viewsets.ModelViewSet):
    queryset = Vcenter.objects.all()
    serializer_class = VcenterSerializers
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=True, methods=['GET'])
    def getallvm(self, request, *args, **kwargs):
        vcenter = self.get_object()
        vimapi = vcenter.vimapi()
        # vm_info = vimapi.get_all_vminfo()
        # vm_info = vimapi.get_one_vminfo_byip(ip='192.168.132.134')
        # vm_info = vimapi.get_all_esxi()
        vm_info = vimapi.get_obj()
        with open('vminfo.txt', 'a') as f:
            f.write(str(vm_info))

        return Response(str((vm_info)))

    @action(detail=True, methods=['GET'])
    def getComputeResource(self, request, *args, **kwargs):
        vcenter = self.get_object()
        serializer = self.get_serializer(vcenter)
        content = vcenter.connect()
        datacenters = content.rootFolder.childEntity
        computeResourceList = []
        for datacenter in datacenters:
            if hasattr(datacenter.hostFolder, "childEntity"):
                hostFolder = datacenter.hostFolder
                computeResourceList = getComputeResource(hostFolder, computeResourceList)

        return Response(str(computeResourceList))

    @action(detail=True, methods=['GET'])
    def getVcenterInfo(self, request, *args, **kwargs):
        vcenter = self.get_object()
        serializer = self.get_serializer(vcenter)
        content = vcenter.connect()
        vcenterInfo = parse_service_instance(content)
        return Response(str(vcenterInfo))

    @action(detail=False, methods=['GET'])
    def getCustomSpec(self, request, *args, **kwargs):
        vcenter = self.get_object()
        content = vcenter.connect()

        custsepc = getSepc(content)


class VMViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializers
    permission_classes = (permissions.IsAuthenticated,)
