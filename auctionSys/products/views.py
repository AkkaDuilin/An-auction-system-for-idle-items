from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import ProductType, ProductInfo
from django.core.paginator import Paginator
# Create your views here.


class Index(View):
     

    def index(request):


        return render(request, 'product/index.html')
        #return HttpResponse("this is product index page")


    # 显示商品列表，排序选择信息通过context传递 使用正则表达式 (?P<name>pattern) 传参 然后返回对应的list.html
    def pro_list(request, type_id, page, sort):
        product_type = ProductType.objects.get(pk=int(type_id))
        latest_products = ProductInfo.objects.filter(product_type_id=int(type_id)).order_by('-id')[:2]
        if sort == '1':
            products = ProductInfo.objects.filter(product_type_id=int(type_id)).order_by('-id')
        if sort == '2':
            products = ProductInfo.objects.filter(product_type_id=int(type_id)).order_by('-product_price')
        if sort == '3':
            products = ProductInfo.objects.filter(product_type_id=int(type_id)).order_by('-product_click')
        paginator = Paginator(products, 10)
        page = paginator.page(int(page))
        context = {'title':product_type.type_name + '-商品列表',
                'product_type':product_type,
                'latest_products':latest_products,
                'sort':sort,
                'paginator':paginator,
                'page':page}
        return render(request, 'product/list.html')

    # 正则表达式传参
    def detail(request, id):
        product = ProductInfo.objects.get(pk=int(id))
        product.product_click += 1 # 点击量+1
        product.save()
        # 新品推荐
        latest_products = ProductInfo.objects.filter(product_type_id=product.product_type_id).order_by('-id')[:2]
        context = {'title':'商品详情',
               'product':product,
               'latest_products':latest_products}
        res = render(request, 'product/detail.html', context)

        # 记录最近浏览，在用户中心使用
        view_products = request.COOKIES.get('view_products', '')
        product_id = str(product.id)
        if view_products:
            products_list = view_products.split(',')
            # 先判断长度，如果等于5个，则删除最后一个
            if len(products_list) == 5:
                del products_list[4]
            # 如果该商品已经浏览过，则删除之前的记录，并添加到第一个的位置
            if products_list.count(product_id) == 1:
                products_list.remove(product_id)
            products_list.insert(0, product_id)
            view_products = ','.join(products_list)
        else:
            view_products = product_id
        res.set_cookie('view_products', view_products)
        return res