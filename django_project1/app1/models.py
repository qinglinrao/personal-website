from django.db import models

# Create your models here.

class Person(models.Model):
    # 因为mysql不是默认的数据库，所以用到的Field不一样--todo
    name = models.charField(max_length=30)
    age = models.IntegerField()

