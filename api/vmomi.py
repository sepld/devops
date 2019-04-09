#!/usr/bin/env python
# coding=utf-8


from pyVmomi import vim
from pyVim.connect import SmartConnectNoSSL, Disconnect
import atexit
from vmware.tasks import wait_for_tasks


class VimAPI(object):
    """
    pyvmomi api
    """

    def __init__(self, host, user, pwd, port):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = int(port)
        self._content = None
        self._si = None
        self._containerView = None
        self.connect()

    def connect(self):
        si = SmartConnectNoSSL(host=self.host,
                               user=self.user,
                               pwd=self.pwd,
                               port=self.port)
        content = si.RetrieveContent()
        atexit.register(Disconnect, si)
        self._content = content
        self._si = si

    def get_views(self, viewType, recursive=True):
        """
        获取rootFolder视图
        :param viewType: 实体类型  eg - [vim.VirtualMachine]
        :param recursive:  是否递归Folder
        :return: 实体view列表
        """
        content = self._content
        container = content.rootFolder  # starting point to look into
        viewType = viewType
        recursive = recursive  # whether we should look into it recursively
        self._containerView = content.viewManager.CreateContainerView(
            container, viewType, recursive)
        children = self._containerView.view
        return children

    def get_all_vm(self):
        """
        Print information for a particular virtual machine or recurse into a
        folder with depth protection
        """
        viewType = [vim.VirtualMachine]  # object types to look for
        children = self.get_views(viewType)
        allvm = []
        for child in children:
            kwargs = {}
            kwargs['summary'] = child.summary
            kwargs['config'] = child.config
            kwargs['guest'] = child.guest
            kwargs['datastore'] = child.datastore
            kwargs['network'] = child.network
            allvm.append(kwargs)
        self._containerView.DestroyView()
        return allvm

    def get_one_vm_byip(self, ip=None):
        """
        根据ip获取vminfo
        :param ip:  ip地址
        :return:  虚拟机信息
        """
        allvm = self.get_all_vm()
        onevm = []
        if ip:
            for vminfo in allvm:
                if vminfo['guest'].ipAddress == ip:
                    onevm.append(vminfo)
        return onevm

    def get_all_template(self):
        """
        获取所有的模板
        :return: 模板信息列表
        """
        allvm = self.get_all_vm()
        templates = []
        for vm in allvm:
            if vm['config'].template:
                templates.append(vm)
        return templates

    def get_all_esxi(self):
        viewType = [vim.HostSystem]  # object types to look for
        children = self.get_views(viewType)
        for child in children:
            print(child.config)

    def get_all_datastore(self):
        viewType = [vim.Datastore]
        children = self.get_views(viewType)

#
# def clone_vm(service_instance,
#              content, template, vm_name, si,
#              datacenter_name, vm_folder, datastore_name,
#              cluster_name, resource_pool, power_on, datastorecluster_name):
#     """
#     Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
#     cluster_name, resource_pool, and power_on are all optional.
#     """
#
#     # if none git the first one
#     datacenter = get_obj(content, [vim.Datacenter], datacenter_name)
#
#     if vm_folder:
#         destfolder = get_obj(content, [vim.Folder], vm_folder)
#     else:
#         destfolder = datacenter.vmFolder
#
#     if datastore_name:
#         datastore = get_obj(content, [vim.Datastore], datastore_name)
#     else:
#         datastore = get_obj(
#             content, [vim.Datastore], template.datastore[0].info.name)
#
#     # if None, get the first one
#     cluster = get_obj(content, [vim.ClusterComputeResource], cluster_name)
#
#     if resource_pool:
#         resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)
#     else:
#         resource_pool = cluster.resourcePool
#
#     vmconf = vim.vm.ConfigSpec()
#     print("vmconf: " + str(vmconf) + '\n')
#
#     if datastorecluster_name:
#         podsel = vim.storageDrs.PodSelectionSpec()
#         pod = get_obj(content, [vim.StoragePod], datastorecluster_name)
#         podsel.storagePod = pod
#
#         storagespec = vim.storageDrs.StoragePlacementSpec()
#         storagespec.podSelectionSpec = podsel
#         storagespec.type = 'create'
#         storagespec.folder = destfolder
#         storagespec.resourcePool = resource_pool
#         storagespec.configSpec = vmconf
#
#         try:
#             rec = content.storageResourceManager.RecommendDatastores(
#                 storageSpec=storagespec)
#             rec_action = rec.recommendations[0].action[0]
#             real_datastore_name = rec_action.destination.name
#         except:
#             real_datastore_name = template.datastore[0].info.name
#
#         datastore = get_obj(content, [vim.Datastore], real_datastore_name)
#
#     # set relospec
#     relospec = vim.vm.RelocateSpec()
#     relospec.datastore = datastore
#     relospec.pool = resource_pool
#
#     clonespec = vim.vm.CloneSpec()
#     clonespec.location = relospec
#     # clonespec.powerOn = power_on
#
#     print("cloning VM...")
#     task = template.CloneVM_Task(folder=destfolder, name=vm_name, spec=clonespec)
#     wait_for_tasks(service_instance, [task])
