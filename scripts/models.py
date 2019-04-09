from django.db import models
from user.models import User


# Create your models here.

class Scripts(models.Model):
    script_name = models.CharField(max_length=50)
    script_file = models.TextField()
    script_args = models.CharField(blank=True, null=True, max_length=100)
    script_type = models.CharField(max_length=50)
    script_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
