from django.shortcuts import render
from django.http import HttpResponse
from .models import ProductInfo,ProductType

# Create your views here.
def index(request):
    return render(request, 'product/index.html')
    #return HttpResponse("this is product index page")
    
    
def plist(request, type_id, page, sort):
     return render(request, 'product/list.html')
 
def detail(request, id):
    res = render(request, 'product/detail.html')
    view_products = request.COOKIES.get('view_products', '')
    res.set_cookie('view_products', view_products)
    return res