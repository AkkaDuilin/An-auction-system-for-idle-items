from django.shortcuts import render, redirect
from django.views import View
from .models import AuctionBid, BidderList
from products.models import ProductInfo

class AuctionCreate(View):
    def get(self, request, product_id):
        product = ProductInfo.objects.get(id=product_id)
        context = {
            'product': product
        }
        return render(request, 'auction/create.html', context)

    def post(self, request, product_id):
        product = ProductInfo.objects.get(id=product_id)
        starting_price = request.POST.get('starting_price')
        description = request.POST.get('description') 
        bid_count = request.POST.get('bid_count')
        auction = AuctionInfo.objects.create(
            auction_seller=request.user,  # 使用当前用户作为拍卖卖家
            starting_price=starting_price,
            description=description,
            product=product,
            bid_count=bid_count,
        )

        return redirect('/')


class AuctionDetail(View):
    def get(self, request, auction_id):
        auction = get_object_or_404(AuctionInfo, auction_id=auction_id)
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
            'auction': auction,
            'current_time': current_time,
        }

        return render(request, 'auction/detail.html', context)

class AuctionBid(View):
    
    def post(self, request, auction_id):
        auction = get_object_or_404(AuctionInfo, auction_id=auction_id)
        bid_amount = request.POST.get('bid_amount')
        bidder_id = request.user.id

        # Update current bid and winning bidder
        if bid_amount > auction.current_bid:
            auction.current_bid = bid_amount
            auction.winning_bidder = request.user
            auction.save()

        # Add bidder to bidder list
        bidder, created = Bidder.objects.get_or_create(user_id=bidder_id)
        bidder.bid_amount = bid_amount
        bidder.save()

        if auction.bidder_list:
            bidder_list = auction.bidder_list
        else:
            bidder_list = BidderList.objects.create()

        bidder_list.bidders.add(bidder)
        context = {
            'auction': auction,
            'current_time': current_time,
        }
        return render(request, 'auction/detail.html', context)

