# coding:utf-8

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# from __future__ import unicode_literals
import json, re, sys
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from app1.models import User, Article, Comment
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

    # 获取文章数据
    article_data = Article.objects.filter()
    print('article_data = %s' % article_data)

    return render(request, 'index.html', {'string': string, 'is_login': is_login, 'user_data': user_data, 'article_data': article_data, 'index':1})

def detail(request):
    id = request.GET['id']
    print('文章ID = %s' % id)

    # 获取文章数据
    article = Article.objects.filter(id=id).order_by('-id')
    print('文章数据 = %s' % article)
    # 使用视图模板
    string = "谢谢雷经理，这个是我的简历。"

    # 判断是否登陆
    is_login = request.session.get('is_login', False)
    print('is_login = %s' % is_login)

    # 生成验证码
    # get_code_img()

    # 查询评论列表
    # 排序无效？--todo
    comment_data = Comment.objects.filter(article_id=id)
    print('评论数据 = %s' % comment_data)

    return render(request, 'detail.html', {'string': string, 'article': article[0], 'comment_data':comment_data, 'is_login': is_login, 'id': id})

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

        redis = Redis()
        redis.link()

        # 防刷，不能用token，每次访问都不一样的。
        key = REDIS_WEB_PREFIX + 'register_' + str(user_name)
        print('key = %s' % key)
        redis_token = redis.get(key)
        print('redis_token = %s' % redis_token)
        if redis_token:
            res = {'code': '-1', 'msg': '300秒内不能重复注册'}
            return JsonResponse(res)
        else:
            redis.set(key, 1, 300)

        t = time.time()
        t = int(t)

        data = User.objects.create(name=user_name, email=email, password=md5(str(md5(pwd)) + USER_SALT), ip=get_client_ip(request), add_time=t, last_time=t)

        user_name = data.name
        user_id = data.id

        rand_num = random.randint(100000, 999999)
        token = uuid.uuid5(uuid.NAMESPACE_DNS, str(rand_num))
        print('token = %s' % token)

        data = {'user_id': user_id, 'user_name': user_name, 'user_token': token}

        # 保存登陆状态--todo

        # 设置session过期时间
        request.session.set_expiry(3600)

        request.session['is_login'] = True
        request.session['user_id'] = user_id

        res = {'code': '1', 'msg': '注册成功！', 'data': data}

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

        user_id = 0
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
            request.session.set_expiry(3600)

            request.session['is_login'] = True
            request.session['user_id'] = user_id

            res = {'code': 1, 'msg': '登陆成功！', 'data': data}

            return JsonResponse(res)
        else:
            res = {'code': '-1', 'msg': '登陆失败！'}
        return JsonResponse(res)

    res = {'code': '1', 'msg': '登陆成功2！'}
    return JsonResponse(res)


@csrf_protect
def action_login_out(request):
    # 判断是否登陆
    is_login = request.session.get('is_login', False)
    print('is_login = %s' % is_login)

    if is_login:

        try:
            del request.session['is_login']  # 不存在时报错
            del request.session['user_id']  # 不存在时报错
        except KeyError:
            res = {'code': '1', 'msg': '退出登陆失败！'}
            return JsonResponse(res)

    res = {'code': '1', 'msg': '退出登陆成功！'}
    return JsonResponse(res)

@csrf_protect
def action_comment(request):
    id = request.GET['id']
    content = 0
    if request.method == 'POST':
        content = request.POST['content']
        code = request.POST['code']

        is_login = request.session.get('is_login', False)

        if not is_login:
            return JsonResponse({'code': '-1', 'msg': '请先登陆'})

        if not content or not code:
            return JsonResponse({'code': '-1', 'msg': '缺少参数'})

        if code != request.session['captcha']:
            return JsonResponse({'code': '-1', 'msg': '验证码错误'})

    # 添加评论操作
    redis = Redis()
    redis.link()
    user_id = request.session.get('user_id', False)
    print('user_id = %s' % user_id)
    # 防刷，不能用token，每次访问都不一样的。
    key = REDIS_WEB_PREFIX + 'comment_' + str(user_id)
    print('key = %s' % key)
    redis_token = redis.get(key)
    print('redis_token = %s' % redis_token)
    if redis_token:
        res = {'code': '-1', 'msg': '30秒内不能重复评论'}
        return JsonResponse(res)
    else:
        redis.set(key, 1, 30)

    res = User.objects.filter(id=user_id)
    print('用户：%s' % res)

    if (res):
        for r in res:
            user_name = r.name
            user_id = r.id
    else:
        res = {'code': '-1', 'msg': '用户不存在'}
        return JsonResponse(res)

    t = time.time()
    t = int(t)

    data = Comment.objects.create(content=content, article_id=id, user_id=user_id,user_name=user_name,
                                  father_id=0, add_time=t)

    data = {'content': data.content, 'user_name': user_name, 'add_time': data.add_time}
    res = {'code': '1', 'msg': '评论成功！', 'data': data}
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

# 获取验证码
def captcha(request):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    import random
    from io import BytesIO
    # 实例一个图片对象120 x 60:
    width = 60
    height = 30
    # 图片颜色
    clo = (43, 34, 88)  # 我觉得是紫蓝色
    image = Image.new('RGB', (width, height), clo)

    # 创建Font对象:
    # 字体文件可以使用操作系统的，也可以网上下载
    font = ImageFont.truetype('static/font/Androgyne_TB.otf', 20)

    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    # 输出文字,随机字体
    str = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    str1 = random.sample(str, 4)
    str1 = ''.join(str1)
    # 保存到session
    request.session['captcha'] = str1.lower()

    w = 4  # 距离图片左边距离
    h = 10  # 距离图片上边距离

    draw.text((w, h), str1, font=font)
    # 模糊:
    image.filter(ImageFilter.BLUR)

    # 干扰线颜色。
    linecolor = ((255, 0, 0), (0, 255, 0), (0, 0, 255))

    # 绘制干扰线

    for i in linecolor:
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=i)

    code_name = 'test_code_img.jpg'
    # save_dir = './static/images/code_img/{}'.format(code_name)
    buf = BytesIO()
    image.save(buf, 'jpeg')
    # print("已保存图片: {}".format(save_dir))
    # image_data = open(save_dir, "rb").read()
    return HttpResponse(buf.getvalue(), content_type="image/png")