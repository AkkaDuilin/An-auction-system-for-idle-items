from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .models import Userinfo
from products.models import ProductInfo
from order.models import OrderInfo
from hashlib import sha1
from .decorator import login as user_login
from django.views.generic import View
from itsdangerous import TimedSerializer  as Serializer
from django.contrib.auth import authenticate,logout
from django.conf import settings
from django.urls import reverse
import re

class RegisterView(View):
    '''注册类视图'''
    def get(self, request):
        '''注册页面'''
        return render(request, 'user/register.html')
    
    def post(self, request):
        '''注册处理'''
        # 1、接收数据
        user_name = request.POST.get('user_name')
        user_pwd = request.POST.get('pwd')
        user_email = request.POST.get('email')
        user_cpwd = request.POST.get('cpwd')
        allow = request.POST.get('allow')
        if user_pwd != user_cpwd:
            return redirect('/user/register/', {'errmsg': '请输入相同的两次密码'})

        # 校验user_name在数据库中是否存在
        try:
            user = Userinfo.objects.get(user_name=user_name)
        except Exception as e:
            user = None
        if user:
            # 用户名存在
            return render(request, 'user/register.html', {'errmsg': '用户已存在'})

        # 2、校验数据
        if not all([user_name, user_pwd, user_email]):
            # 数据不完整
            return render(request, 'user/register.html', {'errmsg': '数据不完整'})
        if not re.match('^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', user_email):
            return render(request, 'user/register.html', {'errmsg': '邮箱格式不正确'})
        if allow != 'on':
            return render(request, 'user/register.html', {'errmsg': '请同意协议'})

        # 3、保存进数据库
        user = Userinfo()
        user.user_name = user_name
        user.user_pwd = user_pwd
        user.user_email = user_email
        user.is_active = 0
        user.save()

        # 4、发送邮件验证 http://127.0.0.1:8000/user/register/active/id
        # 对id进行加密
        # serializer = Serializer(settings.SECRET_KEY, 3600)
        # info = {'confirm': user.id}
        # token = serializer.dumps(info).decode('utf8')

        # # 调用celery队列
        # send_register_active_email.delay(user_email, user_name, token)

        # 5、返回应答
        return redirect('/user/login')

# class ActiveView(View):
#     '''邮件认证处理'''
#     def get(self, request, token):
#         try:
#             serializer = Serializer(settings.SECRET_KEY, 3600)
#             res = serializer.loads(token)

#             # 获取用户名id
#             user_id = res['confirm']

#             # 修改数据库
#             user = Userinfo.objects.get(id=user_id)
#             user.is_active = 1
#             user.save()

#             # 跳转到首页
#             return redirect(reverse('user:login'))
#         except SignatureExpired as e:
#             return HttpResponse('验证过期')

class LoginView(View):
    '''登录页面'''

    def get(self, request):
        ##  判断是否记住密码
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'user/login.html', {'username': username, 'checked': checked})

    def post(self, request):
        '''登录校验'''
        ##  1、接收数据
        user_name = request.POST.get('username')
        user_pwd = request.POST.get('pwd')
        remember = request.POST.get('remember')

        ##  2、数据校验
        if not all([user_name, user_pwd]):
            ##  数据不完整
            return render(request, 'user/login.html', {'errmsg': '用户名或密码不正确'})
        
        ##  3、业务处理
        ##  校验数据库
        #user = authenticate(username=username, password=password)
        user = Userinfo.objects.get(user_name=user_name)
        print(user)
        if user_pwd == user.user_pwd:
            print("login right")
            url = request.COOKIES.get('url', '/')
            res = HttpResponseRedirect(url)

            if remember:
                res.set_cookie('username', user_name)
            else:
                res.set_cookie('username', '', max_age=-1)

            request.session['user_id'] = user.id
            request.session['user_name'] = user.user_name

            return res
        else:
            context = {'title':'用户登录', 'username':user_name, 'userpwd':user_pwd, 'error_pwd':1}
            return render(request, 'user/login.html', context)
        

class Logout(View):
    def get(self, request):
        print("the user is logout")
        request.session.flush()
        logout(request)
        return redirect('/')