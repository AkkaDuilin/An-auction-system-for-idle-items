from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import AuctionInfo, BidderList, Bidder
from products.models import ProductInfo 
from user_part.models import UserInfo
from user_part.decorator import login as user_login
from django.utils.decorators import method_decorator
from  django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
import datetime

class AuctionManage(View):
    @user_login
    def detiel(request):
        # 获取当前用户的所有拍卖
        # if not request.user.is_authenticated:
        #     return redirect('/')
        print(request.user)
        user = UserInfo.objects.get(user_name=request.user)
        # user = UserInfo.objects.get(user_name="dyl")
        auctions = AuctionInfo.objects.filter(auction_seller=user)
        context = {
            'auctions': auctions,
        }
        return render(request,'auctions/add_commodity.html',context)
        # return render(request, 'auctions/add_commodity.html',context=context)
        
    @user_login
    def create(request):
        user = UserInfo.objects.get(user_name="dyl")
        starting_price = request.POST.get('starting_price')
        # description = request.POST.get('description') 
        product_name = request.POST.get('product_name')
        product_img = request.FILES.get('product_img')
        product_price = request.POST.get('product_price')
        auction_date = request.POST.get('auction_date')
        product_abstract = request.POST.get('product_abstract')
        product_content = request.POST.get('product_content')
        # 写一个选择框
        product_type = int(request.POST.get('product_type'))
        print(type(product_type))
        print(product_type,product_name,product_img,product_price,product_abstract,product_content)
        # 数据完整性校验
        if not product_name or not product_price  or not product_abstract or not product_content or not product_type:
            print("请填写所有必填字段")
            error_message = "请填写所有必填字段"
            return redirect('/auction/manage/#')
            # return render(request, 'auctions/add_commodity.html', {'error_message': error_message})

        # 其他数据校验
        try:
            product_price = float(product_price)
            if product_price <= 0:
                raise ValueError("商品价格必须大于0")
        except ValueError:
            error_message = "商品价格格式不正确"
            return render(request, 'auctions/add_commodity.html', {'error_message': error_message})

        # 创建商品

        product = ProductInfo.objects.create(
            product_name=product_name,
            product_img=product_img,
            product_price=product_price,
            product_abstract=product_abstract,
            product_content=product_content,
            product_type=product_type
        )
        auction = AuctionInfo.objects.create(
            auction_seller=user,  # 使用当前用户作为拍卖卖家
            starting_price=product_price,
            auction_date = datetime.datetime.strptime(auction_date, '%Y-%m-%dT%H:%M'),
            # auction_final_date = auction_date + datetime.timedelta(days=1)
            # description=description,
            product=product,
            
        )
        # Url需要修改
        print("创建成功")
        return render(request, 'auctions/add_commodity.html')

# 拍卖详情
class AuctionDetail(View):
    @user_login
    def get(self, request, auction_id):
        auction = get_object_or_404(AuctionInfo, id=auction_id)
        current_time = timezone.now()
        # 时间到时获取出价最高者并且关闭拍卖交易
        if current_time > auction.auction_final_date:
            auction.is_Active = False
            highest_bidder = auction.bidder_list.get_highest_bidder()
            if highest_bidder:
                auction.current_bid = highest_bidder.bid_amount
                auction.winning_bidder = highest_bidder.user
            auction.save()
        
        context = {
            'auction_id': auction_id,
            'auction_date': auction.auction_date,
            'auction_final_date': auction.auction_final_date,
            'auction_status': auction.auction_status,
            'product': auction.product,
            'starting_price': auction.starting_price,
            'current_bid': auction.current_bid,
            'winning_bidder': auction.winning_bidder,

            'current_time': current_time,
        }

        res =  render(request, 'auction/detail.html', context)
        viewed_auctions = request.COOKIES.get('viewed_auctions', '')
        if viewed_auctions:
            auctions_list = viewed_auctions.split(',')

            # 最多保存 5 个浏览记录，超过则删除最旧的记录
            if len(auctions_list) == 5:
                del auctions_list[4]

            # 如果当前拍卖已经存在于浏览记录中，则先删除之前的记录
            if auction_id in auctions_list:
                auctions_list.remove(auction_id)

            # 将当前拍卖添加到浏览记录的最前面
            auctions_list.insert(0, auction_id)
            viewed_auctions = ','.join(auctions_list)
        else:
            viewed_auctions = auction_id

        # 设置浏览记录的 Cookie
        res.set_cookie('viewed_auctions', viewed_auctions)

        return res


class AuctionDepositPayment(View):
    @user_login
    def get(self, request, auction_id):
        auction = AuctionInfo.objects.get(auction_id=auction_id)
        user = UserInfo.objects.get(user=request.user)

        # 检查用户的保证金余额是否足够支付
        if user.deposit_balance >= auction.deposit_amount:
            # 创建新的Bidder对象并添加到bidder_list中
            bidder = Bidder.objects.create(
                user=user,
                if_pay_deposit=True,
                bid_amount=auction.starting_price
            )

            # 更新拍卖信息和用户对象
            auction.bidder_list.add(bidder)
            user.deposit_balance -= auction.deposit_amount
            auction.save()
            user.save()

            return redirect('auctions:auction_detail', auction_id=auction_id)
        else:
            error_message = "保证金余额不足"
            context = {'error_message': error_message}
            return render(request, 'auction/detail.html', context)
    
class AuctionBid(View):
    @user_login
    def post(self, request, auction_id):
        auction = get_object_or_404(AuctionInfo, auction_id=auction_id)
        bid_amount = request.POST.get('bid_amount')
        bidder_id = request.user.id

        # Check if user exists in bidder_list
        bidder_list = auction.bidder_list
        if not bidder_list.bidders.filter(user=request.user).exists():
            error_message = '请先缴纳保证金'
            return render(request, 'auction/detail.html', {'errmsg': error_message})

        # Calculate minimum bidding increment
        initial_price = auction.current_bid
        min_increment = initial_price * 0.02

        # Check bid amount against minimum increment and current bid
        if float(bid_amount) >= (auction.current_bid + min_increment):
            # Update current bid and winning bidder
            auction.current_bid = bid_amount
            auction.winning_bidder = request.user
            auction.save()

            # Create or update bidder
            bidder = auction.bidder_list.bidders.get(user=request.user)
            bidder.bid_amount = bid_amount
            bidder.save()

            # Add bidder to bidder list
            auction.bidder_list.save()

            context = {
                'auction': auction,
                'current_time': timezone.now(),
            }
            return render(request, 'auction/detail.html', context)
        else:
            error_message = '竞价金额不能低于最小加价幅度'
            return render(request, 'auction/detail.html', {'errmsg': error_message})


class AuctionDelete(View):
    @user_login
    def post(self, request, auction_id):
        auction = get_object_or_404(AuctionInfo, auction_id=auction_id)
        auction.delete()
        return redirect('auctions/manage/')


class AuctionUpdate(View):
    @user_login
    def get(self, request, auction_id):
        auction = get_object_or_404(AuctionInfo, auction_id=auction_id)
        product = auction.product
        context = {
            'auction': auction,
            'product': product
        }
        return render(request, 'auction/update.html', context)

    def post(self, request, auction_id):
        auction = get_object_or_404(AuctionInfo, auction_id=auction_id)
        product = auction.product
        
        # 获取拍卖信息的字段
        starting_price = request.POST.get('starting_price')
        description = request.POST.get('description') 
        bid_count = request.POST.get('bid_count')

        # 获取商品信息的字段
        product_name = request.POST.get('product_name')
        product_img = request.FILES.get('product_img')
        product_price = request.POST.get('product_price')
        product_abstract = request.POST.get('product_abstract')
        product_content = request.POST.get('product_content')
        product_type_id = request.POST.get('product_type')

        # 更新拍卖信息
        auction.starting_price = starting_price
        auction.description = description
        auction.bid_count = bid_count
        auction.save()

        # 更新商品信息
        product.product_name = product_name
        product.product_img = product_img
        product.product_price = product_price
        product.product_abstract = product_abstract
        product.product_content = product_content
        product.product_type_id = product_type_id
        product.save()

        context = {
            'auction': auction,
            'product': product,
            'message': '拍卖信息和商品信息已成功更新'
        }
        return render(request, 'auction/update.html', context)