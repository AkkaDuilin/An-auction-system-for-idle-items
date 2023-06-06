from django.contrib import admin
from .models import OrderInfo


admin.site.register(OrderInfo, OrderInfoAdmin)