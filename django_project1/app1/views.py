# coding:utf-8

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# from __future__ import unicode_literals
import json, re, sys
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from app1.models import User
import json, hashlib
import time
import random, uuid
sys.path.append('/var/www/html/django_project1/app1/')
from config import USER_SALT, REDIS_WEB_PREFIX
# from redis.config import Redis
# 上面的写法加载不了 --todo
from app1.redis.config import Redis
from http import cookies

def index(request):
    # return HttpResponse(u"第一个app应用2222！")
    if request.method == 'POST':  # 当提交表单时

        form = AddForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            email = form.cleaned_data['email']
            user_name = form.cleaned_data['user_name']
            pwd = form.cleaned_data['user_name']
            return HttpResponse(str(int(email) + int(user_name) + int(pwd)))


    # 判断是否登陆
    is_login = request.session.get('is_login', False)
    print('is_login = %s' % is_login)

    user_data = None
    if is_login:
        user_id = request.session.get('user_id')
        print('user_id = %s' % user_id)
        user_data = User.objects.filter(id=user_id)
        print('user_data：%s' % user_data)


    # 使用视图模板
    string = "谢谢雷经理，这个是我的简历。"
    return render(request, 'index.html', {'string': string, 'is_login': is_login, 'user_data': user_data})

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

        t = time.time()
        t = int(t)

        User.objects.create(name=user_name, email=email, password=md5(str(md5(pwd)) + USER_SALT), ip=get_client_ip(request), add_time=t, last_time=t)

        res = {'code': '1', 'msg': '注册成功！'}
        # for key in request.POST:
        #     print(key)
        return JsonResponse(res)
    res = {'code': '1', 'msg': '注册成功2！'}
    return JsonResponse(res)

@csrf_protect
def action_login(request):

    if request.method == 'POST':

        user_name = request.POST['user_name']
        pwd = request.POST['password']

        if not user_name or not pwd:
            return JsonResponse({'code': '-1', 'msg': '缺少参数'})

        rand_num = random.randint(100000, 999999)
        token = uuid.uuid5(uuid.NAMESPACE_DNS, str(rand_num))
        print('token = %s' % token)

        redis = Redis()
        redis.link()
        
        # 防刷，不能用token，每次访问都不一样的。
        # key = REDIS_WEB_PREFIX + str(token)
        key = REDIS_WEB_PREFIX + 'login_' + str(user_name)
        print('key = %s' % key)
        redis_token = redis.get(key)
        print('redis_token = %s' % redis_token)
        if redis_token:
            res = {'code': '-1', 'msg': '不能重复提交'}
            return JsonResponse(res)
        else:
            redis.set(key, 1, 3)

        t = time.time()
        t = int(t)
        password = md5(str(md5(pwd)) + USER_SALT)

        res = User.objects.filter(name=user_name, password=password)
        print('用户：%s' % res)

        if(res):

            for r in res:
                user_name = r.name
                user_id = r.id

            User.objects.filter(name=user_name, password=password).update(token=token, last_time=t)
            print('user_id = %s' % user_id)
            print('user_name = %s' % user_name)
            data = {'user_id':user_id, 'user_name': user_name, 'user_token': token}

            # 保存登陆状态

            # 设置session过期时间
            request.session.set_expiry(300)

            request.session['is_login'] = True
            request.session['user_id'] = user_id

            res = {'code': 1, 'msg': '登陆成功！', 'data': data}

            return JsonResponse(res)
        else:
            res = {'code': '-1', 'msg': '登陆失败！'}
        return JsonResponse(res)

    res = {'code': '1', 'msg': '登陆成功2！'}
    return JsonResponse(res)

# 判断邮箱格式
def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
        return 0
    return 0

# md5加密
def md5(s):
    mdb_object = hashlib.md5()
    mdb_object.update(s.encode("utf-8"))
    return mdb_object.hexdigest()

# 获取ip地址
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip