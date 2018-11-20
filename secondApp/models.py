from django.db import models

# Create your models here.

class Tomato(models.Model):
    description = models.CharField(max_length=100, default='Tomato object')
    status = models.CharField(max_length=100, default='New')
