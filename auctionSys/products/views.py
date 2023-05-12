from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
# Create your views here.


class Index(View):

    def index(request):


        return render(request, 'product/index.html')
        #return HttpResponse("this is product index page")

    def pro_list(request, type_id, page, sort):


        return render(request, 'product/list.html')

    def detail(request, id):

        res = render(request, 'product/detail.html')