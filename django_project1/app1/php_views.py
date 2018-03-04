from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def php_lab(request):
    return render(request, 'php_lab.html')
