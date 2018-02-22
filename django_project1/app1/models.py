from django.db import models
from DjangoUeditor.models import UEditorField
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
    brief = models.TextField(u'简要')
    #content = models.TextField(u'内容')
    # 整合百度的ueditor编辑器。
    # content = UEditorField(u'内容', height=300, width=1000,
    #                        default=u'默认内容', blank=True, imagePath="uploads/images/",
    #                        toolbars='besttome', filePath='uploads/files/')content = UEditorField(u'内容', height=300, width=1000,
    #                        default=u'默认内容', blank=True, imagePath="uploads/images/",
    #                        toolbars='besttome', filePath='uploads/files/')
    # 这里有问题--todo
    content = UEditorField(u'内容')

    cate_id = models.IntegerField(u'分类id')
    source_name = models.CharField(u'来源网站名称', max_length=50)
    source_url = models.CharField(u'来源网站url', max_length=50)
    source_auther = models.CharField(u'来源网站作者', max_length=30)
    type = models.IntegerField(u'转载或者原创')
    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

# 分类表
class category(models.Model):
    name = models.CharField(u'分类名称', max_length=30)
    father_id = models.IntegerField(u'父级分类id')

# 评论表
class comment(models.Model):
    content = models.CharField(u'评论内容', max_length=30)
    article_id = models.IntegerField(u'文章id')
    user_id = models.IntegerField(u'用户id')
    father_id = models.IntegerField(u'父级评论id')
    add_time = models.IntegerField(u'添加时间')