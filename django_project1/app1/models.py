from django.db import models
# from DjangoUeditor.models import UEditorField
# Create your models here.
from ckeditor.fields import RichTextField
from tinymce.models import HTMLField
import tinymce

# 用户表
class User(models.Model):

    name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    add_time = models.IntegerField()
    last_time = models.IntegerField()
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 文章表
class Article(models.Model):

    title = models.CharField(u'标题', max_length=30)
    auther = models.CharField(u'作者', max_length=30)
    brief = tinymce.models.HTMLField(verbose_name='简要')
    # content = RichTextField('正文')
    # content = models.TextField(u'内容')
    content = tinymce.models.HTMLField(verbose_name='文章详情')

    cate_id = models.IntegerField(u'分类id')
    source_name = models.CharField(u'来源网站名称', max_length=50, default='')
    source_url = models.CharField(u'来源网站url', max_length=50, default='')
    source_auther = models.CharField(u'来源网站作者', max_length=30, default='1')
    type = models.IntegerField(u'转载或者原创')
    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.title

# 分类表
class Category(models.Model):
    name = models.CharField(u'分类名称', max_length=30)
    father_id = models.IntegerField(u'父级分类id')

    def __str__(self):
        return self.name

# 评论表
class Comment(models.Model):
    content = models.CharField(u'评论内容', max_length=300)
    article_id = models.IntegerField(u'文章id')
    user_name = models.CharField(u'用户名称', max_length=30, default='')
    user_id = models.IntegerField(u'用户id')
    father_id = models.IntegerField(u'父级评论id')
    add_time = models.IntegerField(u'添加时间')
    def __str__(self):
        return self.content