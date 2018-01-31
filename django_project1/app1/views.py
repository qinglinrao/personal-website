# coding:utf-8

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    # return HttpResponse(u"第一个app应用2222！")
    
    # 使用视图模板
    string = "模板测试变量"

    print('controller刷新测试')
    print('测试Debug模式自动刷新')
    return render(request, 'index.html', {'string': string})
