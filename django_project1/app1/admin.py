from django.contrib import admin
from .models import User, Article, category, comment

# Register your models here.
admin.site.register(User)
admin.site.register(Article)
admin.site.register(category)
admin.site.register(comment)