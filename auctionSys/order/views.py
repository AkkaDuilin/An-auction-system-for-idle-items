from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import OrderInfo
from user_part.decorator import login as user_login
from user_part.models import UserInfo
from auctions.models import AuctionInfo,Bidder,BidderList
from datetime import datetime
from decimal import Decimal
from django.db import transaction
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from products.models import ProductInfo

class OrderCreate(View):
    @user_login
    def post(self, request, auction_id):
        # 获取当前用户和对应的地址
        user = request.user
        address = user.address  # 假设用户的地址存储在 address 属性中

        # 获取相应的拍卖信息
        auction = AuctionInfo.objects.get(auction_id=auction_id)

        # 创建订单
        order = OrderInfo.objects.create(
            order_id=auction_id,
            order_user=user,
            order_date=timezone.now(),
            order_status=0,
        )


        context = {
            'order': order,
        }
        # Todo
        return render(request, 'order/detail.html', context)

class OrderPayment(View):
    @user_login
    def get(self, request, order_id):
        order = OrderInfo.objects.get(order_id=order_id)

        # 执行订单支付的相关操作
        # ...
        # 修改订单状态
        order.order_status = 1
        order.save()

        return redirect('orders:order_detail', order_id=order_id)

class OrderDelete(View):
    @user_login
    def post(self, request, order_id):
        order = get_object_or_404(OrderInfo, order_id=order_id)
        order.delete()
        return redirect('order_list')  # 假设存在名为'order_list'的URL路由

class OrderDetail(View):
    @user_login
    def get(self, request, order_id):
        order = get_object_or_404(OrderInfo, order_id=order_id)
        context = {
            'order': order,
        }
        return render(request, 'order/detail.html', context)

class OrderList(View):
    @user_login
    def get(self, request):
        orders = OrderInfo.objects.filter(order_user=request.user)
        context = {
            'orders': orders,
        }
        return render(request, 'order/add_commodity.html', context)