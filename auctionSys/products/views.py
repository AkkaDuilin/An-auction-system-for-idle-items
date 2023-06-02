from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import ProductType, ProductInfo
from auctions.models import AuctionInfo
from django.core.paginator import Paginator
# Create your views here.


class Index(View):
     

    def index(request):
        type_names = ['书籍', '交通工具', '电子设备', '电子外设', '本地拍品', '其他']
        type_ids = []

        for type_name in type_names:
            product_type = ProductType.objects.get(type_name=type_name)
            type_ids.append(product_type.id)

        hot_products = {}
        latest_products = {}
        # 返回两个字典，键为Typeid 值为检索出的列表
        for type_id in type_ids:
            hot_products[type_id] = list(ProductInfo.objects.filter(product_type_id=type_id).order_by('-product_click')[:4])
            latest_products[type_id] = list(ProductInfo.objects.filter(product_type_id=type_id).order_by('-id')[:4])

        context = {
            'title': '首页',
            'hot_products': hot_products,
            'latest_products': latest_products,
        }
        return render(request, 'product/index.html', context)


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

# 商品发布类
class Publish(View):
    def Create_pub(request):
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            product_img = request.FILES.get('product_img')
            product_price = request.POST.get('product_price')
            product_unit = request.POST.get('product_unit')
            product_abstract = request.POST.get('product_abstract')
            product_content = request.POST.get('product_content')
            product_type_id = request.POST.get('product_type')

            # 数据完整性校验
            if not product_name or not product_price or not product_unit or not product_abstract or not product_content or not product_type_id:
                error_message = "请填写所有必填字段"
                return render(request, 'product/create.html', {'error_message': error_message})

            # 其他数据校验
            try:
                product_price = float(product_price)
                if product_price <= 0:
                    raise ValueError("商品价格必须大于0")
            except ValueError:
                error_message = "商品价格格式不正确"
                return render(request, 'product/create.html', {'error_message': error_message})

            # 创建商品
            product = ProductInfo.objects.create(
                product_name=product_name,
                product_img=product_img,
                product_price=product_price,
                product_unit=product_unit,
                product_abstract=product_abstract,
                product_content=product_content,
                product_type_id=product_type_id
            )
            return render(request, 'auction/create.html', product_id=product.id)
        return render(request, 'product/create.html')

