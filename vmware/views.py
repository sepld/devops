from vmware.models import *
from vmware.serializers import *
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from api.vmomi import *
from pyVmomi import vim
import itertools


