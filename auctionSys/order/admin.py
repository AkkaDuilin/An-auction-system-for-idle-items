from django.contrib import admin
from .models import OrderInfo, OrderDetailInfo

class OrderDetailInfoInline(admin.TabularInline):
    model = OrderDetailInfo
    extra = 1

class OrderInfoAdmin(admin.ModelAdmin):
    inlines = [OrderDetailInfoInline]

admin.site.register(OrderInfo, OrderInfoAdmin)