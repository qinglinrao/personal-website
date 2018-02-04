# coding:utf-8

from django.http import HttpResponse
from django.shortcuts import render

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


def action_register(request):
    print('注册操作')
    return render(request, 'index.html')