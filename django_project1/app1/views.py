# coding:utf-8

from django.http import HttpResponse

def index(request):
    return HttpResponse(u"第一个app应用123！")
