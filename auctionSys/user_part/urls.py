from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^register/',RegisterView.as_view(),name='register'),##    注册
    # url(r'^active/(?P<token>.*)',ActiveView.as_view(),name='active'),##  验证处理
    url(r'^login/',LoginView.as_view(),name='login'),## 登录页面
    url(r'^logout/', Logout.as_view(), name='logout'),## 退出登录
    url(r'^info/', UserInfoView.info, name='user'),  # 用户中心-详情页
    #url(r'^info/$', info),
    url(r'^order/(\d+)', OrderView.order_page), 
    url(r'^order/', OrderView.order, name='order'),  # 订单页
    url(r'^site/', SiteView.site, name='site'),  # 地址页
]