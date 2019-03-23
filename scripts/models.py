from django.db import models


# Create your models here.

class Scripts(models.Model):
    script_name = models.CharField(max_length=50)
    script_file = models.TextField()
    script_args = models.CharField(blank=True, null=True, max_length=100)
    script_type = models.CharField(max_length=50)
