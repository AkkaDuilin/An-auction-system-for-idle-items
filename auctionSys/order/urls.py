from django.urls import path
from .views import OrderCreate, OrderDelete, OrderDetail

app_name = 'orders'

urlpatterns = [
    path('/create/<str:auction_id>/', OrderCreate.as_view(), name='order_create'),
    path('delete/<str:order_id>/', OrderDelete.as_view(), name='order_delete'),
    path('detail/<str:order_id>/', OrderDetail.as_view(), name='order_detail'),
]
