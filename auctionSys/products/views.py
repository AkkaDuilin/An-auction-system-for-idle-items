import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.core.paginator import Paginator
from .models import *
from auctions.models import *
from user_part.models import *
from user_part.decorator import login as user_login

class Index(View):
    
    def get(self, request):
        type_ids = [1, 2, 3, 4, 5, 6]
        # product_types = ProductType.objects.filter(id__in=type_ids)
        # 筛选出auction_id最大的十五个商品
        auction_products = AuctionInfo.objects.all()[:15]
        # 筛选出时间是昨天之内的商品
        # yesterday = datetime.now().date() - timedelta(days=1)
        # auction_products = AuctionInfo.objects.filter(auction_date__gte=yesterday)
        auction_list =[]
        
        for auction in auction_products:
            product = ProductInfo.objects.get(id=auction.product.id)
            product_img = product.product_img
            # print(product_img)
            auction = {
                'auction_id': auction.id,
                'product_name': product.product_name,
                'img_url': product_img,
                'product_abstract': product.product_abstract,
                'auction_date' : auction.auction_date,
                'auction_final_date': auction.auction_final_date,
                'current_bid': product.product_price,
                'auction_status': auction.auction_status,
                'is_list':False
            }
            auction_list.append(auction)
            # print(auction.current_bid)

        context = {
            'title': '首页',
            'auction_list': auction_list,
        }


        return render(request, 'product/index.html', context)


class ProductListView(View):

    def get(self,request,type_id):
        print('list')
        product_type = ['书籍', '交通工具', '电子设备', '电子外设', '本地拍品', '其他']
        
        # 返回对应type的所有Product_id
        url = '{}/'.format(type_id)
        product_ids = ProductInfo.objects.filter(product_type=type_id).values('id')
        product_ids = [product_id['id'] for product_id in product_ids]
        print(product_ids)
        # 获取所有对应商品的拍卖详情
        auction_products = AuctionInfo.get_auctions_by_product_ids(product_ids)
        print(auction_products)
        # print(auction_products)

        # paginator = Paginator(auction_products, 10)
        # page = paginator.page(int(page))
        
        auction_list =[]       
        for auction in auction_products:
            product = ProductInfo.objects.get(id=auction.product.id)
            product_img = product.product_img
            # print(product_img)
            auction = {
                'auction_id': auction.id,
                'product_name': product.product_name,
                'img_url': product_img,
                'product_abstract': product.product_abstract,
                'auction_date' : auction.auction_date,
                'auction_final_date': auction.auction_final_date,
                'current_bid': product.product_price,
                'auction_status': auction.auction_status,
                'is_list':True
            }
            auction_list.append(auction)
            # print(auction.current_bid)

        context = {
            'title': '首页',
            'auction_list': auction_list,
        }

        return render(request, 'product/index.html',context)
        # return redirect(url,context)

