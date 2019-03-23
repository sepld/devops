from django.db import models


# Create your models here.

class Servers(models.Model):
    ip = models.CharField(max_length=100)
