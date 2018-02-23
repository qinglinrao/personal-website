from django.db import models
# from DjangoUeditor.models import UEditorField
# Create your models here.
from ckeditor.fields import RichTextField

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
    brief = models.TextField(u'简要', default='')
    # content = RichTextField()
    content = models.TextField(u'简要')

    cate_id = models.IntegerField(u'分类id')
    source_name = models.CharField(u'来源网站名称', max_length=50, default='')
    source_url = models.CharField(u'来源网站url', max_length=50, default='')
    source_auther = models.CharField(u'来源网站作者', max_length=30, default='1')
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