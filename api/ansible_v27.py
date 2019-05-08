#!/usr/bin/env python

import json
import shutil
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


class Options(object):
    def __init__(self,
                 connection='local',
                 module_path=None,
                 forks=None,
                 remote_user=None,
                 conn_pass=None,
                 become=False,
                 become_method=None,
                 become_user=None,
                 become_pass=None,
                 check=False,
                 diff=False,
                 gather_facts=None,
                 private_key_file=None,
                 ssh_args=None,
                 host_key_checking=None
                 ):
        self.connection = connection
        self.module_path = module_path
        self.forks = forks
        self.become = become
        self.become_method = become_method
        self.become_user = become_user
        self.become_pass = become_pass
        self.remote_user = remote_user
        self.conn_pass = conn_pass
        self.check = check
        self.diff = diff
        self.gather_faces = gather_facts
        self.private_key_file = private_key_file
        self.ssh_args = ssh_args
        self.host_key_checking = host_key_checking


class BaseAnsible(object):
    def __init__(self, host_list, remote_user, conn_pass=None, become_pass=None):
        self.options = Options()
        self.options.connection = 'smart'
        self.options.gather_faces = 'no'
        self.options.forks = 100
        self.options.check = False
        self.options.remote_user = remote_user
        self.options.conn_pass = conn_pass
        self.options.become_pass = become_pass
        self.options.become = True
        self.options.become_method = 'sudo'
        self.options.become_user = 'root'

        # self.options.private_key_file = self.set_private_file()

        self.host_list = host_list

        self.loader = DataLoader()
        self.results_callback = ResultCallback()
        self.inventory = InventoryManager(loader=self.loader, sources=self.host_list)
        self.variable_manager = VariableManager(loader=self.loader,
                                                inventory=self.inventory)
        self.play_source = None
        self.passwords = self.build_passwords()
        C.HOST_KEY_CHECKING = False  # 关闭主机密钥检查

    def set_private_file(self):
        private_file = '/home/ld/.ssh/id_rsa'
        return private_file

    def build_play_source(self, name='no', hosts='all', tasks=None):
        play_source = dict(
            name=name,
            hosts=hosts,
            gather_facts=self.options.gather_faces,
            tasks=tasks)
        self.play_source = play_source

    def build_passwords(self):
        passwords = dict(
            # conn_pass=self.options.conn_pass,
            become_pass=self.options.become_pass
        )
        return passwords

    def run_play(self):

        play = Play().load(self.play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                # stdout_callback=self.results_callback,
            )
            result = tqm.run(play)
            print(result)
        finally:

            if tqm is not None:
                tqm.cleanup()

            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)


if __name__ == "__main__":
    with open('/home/ld/.ssh/id_rsa.pub') as f:
        key = f.read()

    hostslist = '192.168.132.129'
    if isinstance(hostslist, str):
        hostslist = hostslist + ','

    ansible = BaseAnsible(hostslist, 'ld', '', 'admin')
    print(ansible.options.private_key_file)
    name = 'run ping'
    tasks = [
        dict(action=dict(module='file', args=dict(state="directory", path="/etc/test1"))),
        # dict(action=dict(module='ping')),
        # dict(action=dict(module='authorized_key', args=dict(user='ld', key=key))),
    ]

    ansible.build_play_source(name=name, tasks=tasks)
    ansible.run_play()
