from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$', Index.index),
    url(r'^list(\d+)_(\d+)_(\d+)/$', Index.pro_list),
    url(r'^(\d+)/$', Index.detail)
]