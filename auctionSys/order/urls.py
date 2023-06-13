from django.conf.urls import url
from .views import *


urlpatterns = [
    # ...
    url(r'^create/$', OrderCreate.create, name='order_create'),
    url(r'^list/', OrderList.list, name='order_list'),
    url(r'^deliver/', OrderDeliver.deliver, name='order_list'),
    url(r'^pay/',OrderPayment.pay,name='order_pay'),
    # ...
]
