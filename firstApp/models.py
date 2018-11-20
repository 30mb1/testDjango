from django.db import models

# Create your models here.

class Potato(models.Model):
    description = models.CharField(max_length=100, default='Potato object')
    status = models.CharField(max_length=100, default='New')
