# Generated by Django 2.1 on 2018-03-05 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_auto_20180304_0226'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user_name',
            field=models.CharField(default='', max_length=30, verbose_name='用户名称'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=300, verbose_name='评论内容'),
        ),
    ]
