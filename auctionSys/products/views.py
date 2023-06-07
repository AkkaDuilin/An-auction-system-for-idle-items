import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.core.paginator import Paginator
from .models import *
from auctions.models import *
from user_part.models import *

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
            product = ProductInfo.objects.get(pk=auction.product)
            auction = {
                'auction_id': auction.id,
                'product_name': product.product_name,
                'img_url': product.product_image.url,
                'product_abstract': product.product_abstract,
                'auction_date' : auction.auction_date,
                'auction_finish_date': auction.auction_finish_date,
                'current_price': auction.current_price,
                'auction_status': auction.auction_status,
            }
            auction_list.append(auction)


        context = {
            'title': '首页',
            'auction_list': auction_list,
        }


        return render(request, 'product/index.html', context)


class ProductListView(View):
    def get(self, request, type_id, page, sort):
        

        product_type = ['书籍', '交通工具', '电子设备', '电子外设', '本地拍品', '其他']
        # 返回对应type的所有Product_id
        product_ids = ProductInfo.objects.filter(product_type=type_id).values('id')
        # 获取所有对应商品的拍卖详情
        auction_products = AuctionInfo.get_auctions_by_product_ids(product_ids)
        if sort == '1':
            auction_products = AuctionInfo.get_auctions_by_product_ids(product_ids)
        elif sort == '2':
            auction_products = AuctionInfo.get_auctions_by_product_ids(product_ids).order_by('-current_price')
        elif sort == '3':
            auction_products = AuctionInfo.get_auctions_by_product_ids(product_ids).order_by('-bid_count')

        paginator = Paginator(auction_products, 10)
        page = paginator.page(int(page))
        
        context = {
            'title': f'{product_type[product_ids]}-商品列表',
            'product_type': product_type,
            'auction_products': auction_products,
            'sort': sort,
            'paginator': paginator,
            'page': page
        }
        return render(request, 'product/list.html', context)


class ProductDetailView(View):
    def get(self, request, id):
        product = ProductInfo.objects.get(pk=id)
        product.product_click += 1
        product.save()

        latest_products = ProductInfo.objects.filter(product_type_id=product.product_type_id).order_by('-id')[:2]
        
        context = {
            'title': '商品详情',
            'product': product,
            'latest_products': latest_products
        }
        res = render(request, 'product/detail.html', context)

        # view_products = request.COOKIES.get('view_products', '')
        # product_id = str(product.id)

        # if view_products:
        #     products_list = view_products.split(',')
        #     if len(products_list) == 5:
        #         del products_list[4]

        #     if products_list.count(product_id) == 1:
        #         products_list.remove(product_id)

        #     products_list.insert(0, product_id)
        #     view_products = ','.join(products_list)
        # else:
        #     view_products = product_id

        # res.set_cookie('view_products', view_products)
        return res
