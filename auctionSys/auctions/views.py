from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
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
from decimal import *

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
            # 返回原来的页面
            # return redirect('/')
            return render(request, 'auctions/add_commodity.html', {'error_message': error_message})
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
        bidder_list = BidderList.objects.create()
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
            bidder_list = bidder_list
            
        )
        # Url需要修改
        print("创建成功")
        return redirect('/auction/manage/')

# 拍卖详情
class AuctionDetail(View):
    @user_login
    def detail(request, auction_id):
        print("进入拍卖详情")
        auction = get_object_or_404(AuctionInfo, id=auction_id)
        auction.auction_date = int(auction.auction_date.timestamp())
        current_time = timezone.now()
        # 时间到时获取出价最高者并且关闭拍卖交易
        # if current_time > auction.auction_final_date:
        #     auction.is_Active = False
        #     highest_bidder = auction.bidder_list.get_highest_bidder()
        #     if highest_bidder:
        #         auction.current_bid = highest_bidder.bid_amount
        #         auction.winning_bidder = highest_bidder.user
        #     auction.save()
        # 获取bidder_list的长度
        if auction.bidder_list == None:
            bidder_count = 0
            reverse_count = 0
        else:
            bidder_count = auction.bidder_list.get_bidders_count()
            reverse_count = auction.bidder_list.get_reverse_count()
        print(bidder_count)
        bidders = list(auction.bidder_list.bidders.values_list())
        Bidder_list = []
        for i in bidders:
            Bidder_list.append(Bidder.objects.get(id=i[0]))
        # bidders = list(auction.bidder_list)
        print(Bidder_list)
        # 计算所有if_pay_is_true为false的bidder的总人数
        
        context = {
            'auction_seller': auction.auction_seller,
            'auction_id': auction_id,
            'auction_date': auction.auction_date,
            'auction_final_date': auction.auction_final_date,
            'auction_status': auction.auction_status,
            'product': auction.product,
            'starting_price': auction.starting_price,
            'current_bid': auction.current_bid,
            'winning_bidder': auction.winning_bidder,
            'bidder_count' : bidder_count,
            'current_time': current_time,
            'bidder_list': Bidder_list,
            'reverse_count':reverse_count
        }
        context['errmsg'] = request.session.get('errmsg')
        res =  render(request, 'auctions/detail.html', context)
        request.session['errmsg'] = None
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

class Auctionreverse(View):
    @user_login
    def reverse(request, auction_id):
        print('reverse')
        auction = AuctionInfo.objects.get(id=auction_id)
        user = UserInfo.objects.get(user_name=request.user)
        url = '/auction/{}/'.format(auction_id)
        if auction.bidder_list == None:
            auction.bidder_list = BidderList.objects.create()
        bidder_list = auction.bidder_list
        bidder_exist = bidder_list.bidders.filter(user=user).exists()
        print(bidder_exist)
        # print(bidder_list.bidders_set.all())
        if bidder_exist and bidder_list.bidders.filter(auction_id=auction_id).exists() :
            print('have reserve')
            error_message = "已预约"
            request.session['errmsg'] = error_message
            return redirect(url)
        else:
            bidder = Bidder.objects.create(
                auction_id = auction_id,
                user=user,
                if_pay_deposit=False,
                bid_amount=-1
            )
            # 更新拍卖信息和用户对象
            auction.bidder_list.bidders.add(bidder)
            auction.save()
            user.save()
            return redirect(url, auction_id=auction_id)


class AuctionDepositPayment(View):
    @user_login
    def deposit(request, auction_id):
        print('Deposit')
        auction = AuctionInfo.objects.get(id=auction_id)
        user = UserInfo.objects.get(user_name=request.user)
        url = '/auction/{}/'.format(auction_id)
        # print(auction.bidder_list.bidders.filter(user==user))
        # 检查用户的保证金余额是否足够支付
        #return redirect(url, auction_id=auction_id)
        # 如果保证金大于starting_price的10%
        if auction.bidder_list == None:
            auction.bidder_list = BidderList.objects.create()
        if BidderList.objects.filter(bidders__user=user).exists() and BidderList.objects.filter(bidders__auction_id=auction_id).exists() :
            bidder = Bidder.objects.get(user=user, auction_id=auction_id)
            if  bidder.if_pay_deposit == True:
                error_message = "已交保证金"
                print(error_message)
                request.session['errmsg'] = error_message
                return redirect(url)
            else:
                if user.deposit_balance >= auction.starting_price*Decimal(0.1):
                    # 创建新的Bidder对象并添加到bidder_list中
                    print('update bidder')
                    bidder = Bidder.objects.get(user=user, auction_id=auction_id)
                    # 更新拍卖信息和用户对象
                    bidder.bid_amount = 0
                    bidder.if_pay_deposit = True
                    user.deposit_balance -= auction.starting_price*Decimal(0.1)
                    bidder.save()
                    # auction.save()
                    user.save()
                    # 返回拍卖详情页面
                    return redirect(url, auction_id=auction_id)

                else:
                    print('add bidder failed')
                    error_message = "保证金余额不足"
                    request.session['errmsg'] = error_message
                    return redirect(url)
        
        else:
            print('not reserve')
            error_message = "未预约"
            request.session['errmsg'] = error_message
            return redirect(url)

        
        

class AuctionBid(View):
    @user_login
    def bid(request, auction_id):
        print('Bid')
        auction = get_object_or_404(AuctionInfo, id=auction_id)
        url = '/auction/{}/'.format(auction_id)
        if request.POST.get('bid_amount') == '':
            bid_amount = auction.current_bid
        else:
            bid_amount = request.POST.get('bid_amount')
        print('Bid',bid_amount)
        user = request.user
        user = UserInfo.objects.get(user_name=user)
        if not Bidder.objects.filter(user=user, auction_id=auction_id).exists():
            print('bidder not exist')
            error_message = '请先缴纳保证金'
            request.session['errmsg'] = error_message
            return redirect(url, {'errmsg': error_message})
        bidder = Bidder.objects.get(user=user, auction_id=auction_id)
        

        # Calculate minimum bidding increment
        if auction.current_bid == None:
            auction.current_bid = auction.starting_price
        initial_price = auction.current_bid
        min_increment = float(initial_price) * 0.02

        # Check bid amount against minimum increment and current bid
        if float(bid_amount) >= ( float(initial_price) + min_increment):
            # Update current bid and winning bidder
            print('bid success')
            auction.current_bid = bid_amount
            auction.winning_bidder = bidder
            auction.save()

            # Create or update bidder
            
            bidder.bid_amount = bid_amount
            bidder.save()

            # Add bidder to bidder list
            auction.bidder_list.save()

            context = {
                'auction': auction,
                'current_time': timezone.now(),
            }
            return redirect(url,context)
        else:
            print('bid failed')
            error_message = '竞价金额不能低于最小加价幅度'
            context =  {'errmsg': error_message}
            request.session['errmsg'] = error_message
            #return render(request, 'auctions/detail.html', context)
            return redirect(url,context)


class AuctionDelete(View):
    @user_login
    def delete( request, auction_id):
        print('删除拍品')
        auction = get_object_or_404(AuctionInfo, id=auction_id)
        auction.delete()
        return redirect('/auction/manage/')


class AuctionUpdate(View):
    @user_login
    def detail(request,auction_id):
        # auction_id = 1
        print(request.user)
        
        auction = get_object_or_404(AuctionInfo, id=auction_id)
        print(auction)
        product = auction.product
        context = {
            'auction': auction,
            'product': product
        }
        print(type(auction.auction_date))
        return render(request, 'auctions/product_edit.html', context)

    def update(request, auction_id):
        print('更新拍品')
        auction = get_object_or_404(AuctionInfo, id=auction_id)
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
        product_type = request.POST.get('product_type')

        # 更新拍卖信息
        auction.starting_price = product_price
        # auction.bid_count = bid_count
        auction.save()

        # 更新商品信息
        product.product_name = product_name
        product.product_img = product_img
        product.product_price = product_price
        product.product_abstract = product_abstract
        product.product_content = product_content
        product.product_type = product_type
        product.save()

        context = {
            'auction': auction,
            'product': product,
            'message': '拍卖信息和商品信息已成功更新'
        }
        return redirect('/auction/manage/')