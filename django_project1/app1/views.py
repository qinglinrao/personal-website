# coding:utf-8

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect

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
        # List = ['自强学堂', '渲染Json到模板']
        # Data = {'site': '自强学堂', 'author': '涂伟忠'}
        # return render(request, 'index.html', {
            # 'List': json.dumps(List),
            # 'Data': json.dumps(Data)
        # })
        data = {'code': '1', 'res': '注册成功1！'}
        for key in request.POST:
            print(key)
        return JsonResponse(data)
    data = {'code': '1', 'res': '注册成功2！'}
    return JsonResponse(data)
