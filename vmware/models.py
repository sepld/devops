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


class IpUsage(models.Model):
    ipaddress = models.GenericIPAddressField()
