from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^register/$',RegisterView.as_view(),name='register'),##    注册
    url(r'^logout/$', Logout.as_view(), name='logout'),## 退出登录
    url(r'^info/$', UserInfoView.info, name='user'),  # 用户中心-详情页
    url(r'^history/', UserHistoryView.as_view(), name='user_history'),
    url(r'^site/$', SiteView.site, name='site'),  # 地址页
    url(r'^login/$', LoginView.login),
    url(r'^login_handler/$', LoginView.login_handler),
    url(r'^service/$', ServiceView.as_view(), name='service'),
]