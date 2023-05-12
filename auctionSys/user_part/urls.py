from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^register/$',RegisterView.as_view(),name='register'),##    注册
    # url(r'^active/(?P<token>.*)',ActiveView.as_view(),name='active'),##  验证处理
    url(r'^login/$',LoginView.as_view(),name='login'),## 登录页面
    url(r'^logout/$', Logout.as_view(), name='logout'),## 退出登录
    url(r'^info/$', UserInfoView.as_view(), name='user'),  # 用户中心-详情页
    url(r'^order/$', OrderView.as_view(), name='order'),  # 订单页
    url(r'^site/$', SiteView.as_view(), name='address'),  # 地址页
]