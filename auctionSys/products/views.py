from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):


    return render(request, 'product/index.html')
    #return HttpResponse("this is product index page")