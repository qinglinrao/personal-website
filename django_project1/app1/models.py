from django.db import models

# Create your models here.

# 用户表
class User(models.Model):

    name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    add_time = models.IntegerField()
    last_time = models.IntegerField()
    token = models.CharField(max_length=100)

# 文章表
class Article(models.Model):

    title = models.CharField(u'标题', max_length=30)
    auther = models.CharField(u'作者', max_length=30)
    content = models.TextField(u'内容')
    source = models.CharField(u'来源', max_length=50)
    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)