# coding:utf-8

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    # return HttpResponse(u"第一个app应用2222！")
    
    # 使用视图模板
    return render(request, 'index.html')
