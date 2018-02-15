from django.db import models

# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    add_time = models.IntegerField()
    last_time = models.IntegerField()
    token = models.CharField(max_length=100)

