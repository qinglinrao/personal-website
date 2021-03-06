"""django_project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# 新增一个应用的页面
from app1 import views as app1_views
from app1 import php_views as php_views
from DjangoUeditor import urls as DjangoUeditor_urls

from django.conf import settings
from django.conf.urls import include, url

urlpatterns = [
    # 新增一个应用的页面
    path('', app1_views.index),
    path('detail/', app1_views.detail),
    path('admin/', admin.site.urls),
    # 注册
    path('action_register/', app1_views.action_register),
    # 登陆
    path('action_login/', app1_views.action_login),
    # 退出登陆
    path('action_login_out/', app1_views.action_login_out),
    # 验证码
    path('captcha/', app1_views.captcha),
    # 提交评论
    path('action_comment/', app1_views.action_comment),
    path('ckeditor', include('ckeditor_uploader.urls')),
    # php实验室
    path('php_lab/', php_views.php_lab),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


