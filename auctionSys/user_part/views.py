from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .models import UserInfo
from products.models import ProductInfo
from order.models import OrderInfo
from auctions.models import AuctionInfo
from hashlib import sha1
from .decorator import login as user_login
from django.views.generic import View
from itsdangerous import TimedSerializer as Serializer
from django.contrib.auth import authenticate,logout
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth

import re

class RegisterView(View):
    '''注册类视图'''
    def get(self, request):
        '''注册页面'''
        return render(request, 'user/register.html')
    @csrf_exempt
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
            user = UserInfo.objects.get(user_name=user_name)
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
        user = UserInfo()
        user.user_name = user_name
        user.user_pwd = user_pwd
        user.user_email = user_email
        user.is_active = 0
        user.save()
        User.objects.create_user(user_name,user_email,user_pwd)
        user_obj = auth.authenticate(username=user_name, password=user_pwd)
        
        # 4、发送邮件验证 http://127.0.0.1:8000/user/register/active/id
        # 对id进行加密
        # serializer = Serializer(settings.SECRET_KEY, 3600)
        # info = {'confirm': user.id}
        # token = serializer.dumps(info).decode('utf8')

        # # 调用celery队列
        # send_register_active_email.delay(user_email, user_name, token)

        # 5、返回应答
        return redirect('/user/login/')

# class ActiveView(View):
#     '''邮件认证处理'''
#     def get(self, request, token):
#         try:
#             serializer = Serializer(settings.SECRET_KEY, 3600)
#             res = serializer.loads(token)

#             # 获取用户名id
#             user_id = res['confirm']

#             # 修改数据库
#             user = UserInfo.objects.get(id=user_id)
#             user.is_active = 1
#             user.save()

#             # 跳转到首页
#             return redirect(reverse('user:login'))
#         except SignatureExpired as e:
#             return HttpResponse('验证过期')

class LoginView(View):
    '''登录页面'''
    @csrf_exempt
    def login(request):
        username = request.COOKIES.get('username', '')
        context = {'title':'用户登录', 'username':username, 'error_pwd':0}
        return render(request, 'user/login.html', context)
    # def get(self, request):
    #     ##  判断是否记住密码
    #     if 'username' in request.COOKIES:
    #         username = request.COOKIES['username']
    #         checked = 'checked'
    #     else:
    #         username = ''
    #         checked = ''
    #     return render(request, 'user/login.html', {'username': username, 'checked': checked})
    @csrf_exempt
    def login_judge(request):
        get_datas = request.GET['user_name']
        count = UserInfo.objects.filter(user_name=get_datas).count()
        return JsonResponse({'count': count})
    @csrf_exempt
    def login_handler(request):
        post_datas = request.POST
        user_name = post_datas['username']
        user_pwd = post_datas['pwd']
        remember = post_datas.get('remember', 0)
        # user_obj = authenticate(username=user_name, password=user_pwd)
        user = UserInfo.objects.filter(user_name=user_name, user_pwd=user_pwd).first()
        # 找到用户，判断密码是否一致，若不一致
        #user = UserInfo.objects.get(user_name=user_name)
        if user:
            # login(request, user_obj)
            url = request.COOKIES.get('url', '/')
            res = redirect("/")
            res.set_signed_cookie("is_login","1",salt="auctionSys")
            # if remember:
            #     res.set_cookie('username', user_name)
            # else:
            #     res.set_cookie('username', '', max_age=-1)
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.user_name
            user_obj = auth.authenticate(username=user_name, password=user_pwd)
            auth.login(request, user_obj)
            print(res)
            return res
        else:
            print("the user is not exist")
            context = {'title':'用户登录', 'username':user_name, 'userpwd':user_pwd, 'error_pwd':1}
            return render(request, 'user/login.html', context)
        

class Logout(View):
    def get(self, request):
        print("the user is logout")
        if request.session.get('is_login', None):
            # 清空session
            request.session.flush()

        # logout(request)
        return redirect('/')


class UserInfoView(View):
    '''用户中心-详情页'''
    @user_login
    def info(request):
        print(request.user)
        user_email = UserInfo.objects.get(id=request.session['user_id']).user_email
        
        context = {'title':'个人信息',
                'user_name':request.session['user_name'],
                'user_email':user_email,
                }
        # 发送一个request 给user_center html界面并传递context内容 
        return render(request, 'user/user_center_info.html', context)
    
class UserHistoryView(View):

    def get(self, request):
        
        viewed_auctions = request.COOKIES.get('viewed_auctions', '')
        if viewed_auctions == '':
            return render(request, 'user/b_history.html', {'title':'用户中心-浏览记录'})
        # 这里get的viewed_auctions 对应最近浏览的记录 在auctions view.py detail 中实现
        # 可以阉割
        else:
            view_list = []
            if viewed_auctions:
                viewed_auctions = viewed_auctions.split(',')
                for each in viewed_auctions:
                    view_list.append(AuctionInfo.objects.get(id=int(each)))
            context = {'title':'用户中心-浏览记录',
                    'view_list':view_list}
            return render(request, 'user/b_history.html', context)


class OrderView(View):
    '''用户中心-订单页'''

    # 处理没有指定页码的订单
    @user_login
    def order(request):
        '''显示用户订单页'''
        user_id = request.session['user_id']
        orders = OrderInfo.objects.filter(order_user_id=user_id).order_by('-order_date')
        # paginator 分页类 每页显示2个订单信息 
        # 在前端中使用 for each in paginator.page_range 调用每一页的页号
        paginator = Paginator(orders, 2)
        page = paginator.page(1)
        context = {'title':'全部订单',
                'orders':orders,
                'paginator': paginator,
                'page': page}
        return render(request, 'user/user_center_order.html', context)
        #return render(request, 'user/user_center_order.html', {'page': 'order'})

    # 处理有页码指定的订单 未测试
    @user_login
    def order_page(request, page):
        user_id = request.session['user_id']
        orders = OrderInfo.objects.filter(order_user_id=user_id).order_by('-order_date')
        print(orders)
        paginator = Paginator(orders, 2)
        page = paginator.page(int(page))
        context = {'title':'全部订单',
                'orders':orders,
                'paginator': paginator,
                'page': page}
        return render(request, 'user/user_center_order.html', context)




class SiteView(View):
    '''用户中心-地址页'''
    @user_login
    def site(request):
        '''显示用户地址页'''
        user = UserInfo.objects.get(id=request.session['user_id'])
        if request.method == 'POST':
            user.user_rman = request.POST.get('rman')
            user.user_address = request.POST.get('address')
            user.user_mnumber = request.POST.get('mnumber')
            user.user_pnumber = request.POST.get('pnumber')
            user.save()
        context = {'title':'收货地址', 'user':user}
        return render(request, 'user/user_center_site.html', context)


