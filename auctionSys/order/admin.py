from django.contrib import admin
from .models import OrderInfo

class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_user', 'order_date', 'order_status')
    search_fields = ('order_id', 'order_user', 'order_date', 'order_status')
    list_filter = ('order_id', 'order_user', 'order_date', 'order_status')

class OrderInfoInline(admin.TabularInline):
    model = OrderInfo
    extra = 1

admin.site.register(OrderInfo, OrderInfoAdmin)