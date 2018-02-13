# coding:utf-8

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# from __future__ import unicode_literals
import json, re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from app1.models import User

def index(request):
    # return HttpResponse(u"第一个app应用2222！")
    if request.method == 'POST':  # 当提交表单时

        form = AddForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            email = form.cleaned_data['email']
            user_name = form.cleaned_data['user_name']
            pwd = form.cleaned_data['user_name']
            return HttpResponse(str(int(email) + int(user_name) + int(pwd)))

    # 使用视图模板
    string = "谢谢雷经理，这个是我的简历。"
    return render(request, 'index.html', {'string': string})

def detail(request):
    
    # 使用视图模板
    string = "谢谢雷经理，这个是我的简历。"
    return render(request, 'detail.html', {'string': string})

@csrf_protect
def action_register(request):


    if request.method == 'POST':

        email = request.POST['email']
        user_name = request.POST['user_name']
        pwd = request.POST['pwd']

        if not email or not user_name or not pwd:
            return JsonResponse({'code': '-1', 'msg': '缺少参数'})

        if len(user_name) < 5:
            return JsonResponse({'code': '-1', 'msg': '用户名过短'})

        if len(pwd) < 5:
            return JsonResponse({'code': '-1', 'msg': '密码长度不够'})

        if not validateEmail(email):
            return JsonResponse({'code': '-1', 'msg': '邮箱格式错误'})

        User.objects.create(name=user_name, email=email, password=pwd)

        res = {'code': '1', 'msg': '注册成功！'}
        # for key in request.POST:
        #     print(key)
        return JsonResponse(res)
    res = {'code': '1', 'msg': '注册成功2！'}
    return JsonResponse(res)

# 判断邮箱格式
def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
        return 0
    return 0