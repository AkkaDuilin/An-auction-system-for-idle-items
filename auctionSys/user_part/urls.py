from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^register/',RegisterView.as_view(),name='register'),##    注册
    # url(r'^active/(?P<token>.*)',ActiveView.as_view(),name='active'),##  验证处理
    url(r'^login/',LoginView.as_view(),name='login'),## 登录页面
    url(r'^logout/', Logout.as_view(), name='logout'),## 退出登录
]