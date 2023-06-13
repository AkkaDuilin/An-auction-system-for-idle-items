from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import OrderInfo
from user_part.decorator import login as user_login
from user_part.models import UserInfo
from auctions.models import AuctionInfo,Bidder,BidderList
from datetime import datetime, timezone
from decimal import Decimal
from django.db import transaction
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from products.models import ProductInfo
from django.db.models import Q

class OrderCreate(View):
    @user_login
    def create(request, auction_id):
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
            auction = auction,
            total_price = auction.current_bid,
        )


        context = {
            'order': order,
        }
        # Todo
        return render(request, 'order/create.html', context)

class OrderPayment(View):
    @user_login
    def pay(request):
        # order = OrderInfo.objects.get(order_id=order_id)

        # 执行订单支付的相关操作
        # ...
        # 修改订单状态
        # order.order_status = 1
        # order.save()

        return render(request, 'order/pay.html')

class OrderDelete(View):
    @user_login
    def delete(request, order_id):
        order = get_object_or_404(OrderInfo, order_id=order_id)
        order.delete()
        return redirect('order_list')  # 假设存在名为'order_list'的URL路由

class OrderDetail(View):
    @user_login
    def detail(request, order_id):
        order = get_object_or_404(OrderInfo, order_id=order_id)
        context = {
            'order': order,
        }
        return render(request, 'user_center_order/detail.html', context)

class OrderList(View):
    @user_login
    def list(request):
        print('order')
        user = UserInfo.objects.get(user_name = request.user)
        orders = OrderInfo.objects.filter(order_user=user)
        for order in orders:
            print(orders)
            print(order.order_status)
        context = {
            'orders': orders,
        }
        return render(request, 'user/user_center_order.html', context)
    

class OrderDeliver(View):
    @user_login
    def deliver(request):
        print('order')
        user = UserInfo.objects.get(user_name = request.user)
        # 找到所有order中auction含有auction_seller为当前用户的order
        orders = OrderInfo.objects.filter(
            Q(auction__auction_seller=user)
        )
        order_list = []
        # 返回商品名称，支付状态，价格，买家姓名，买家电话，买家地址，买家邮编
        for order in orders:
            order_content = {
                'order_id': order.order_id,
                'product_name': order.auction.product.product_name,
                'order_status': order.order_status,
                'total_price': order.total_price,
                'user_name': order.order_user.user_name,
                'user_pnumber': order.order_user.user_pnumber,
                'user_address': order.order_user.user_address,
                'user_mnumber': order.order_user.user_mnumber, 

            }
            order_list.append(order_content)

        print(order_list)
        context = {
            'order_list': order_list,
        }
        # return render(request, 'order/deal.html')
        return render(request, 'order/deal.html', context)
    
