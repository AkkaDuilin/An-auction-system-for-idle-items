from django.conf.urls import url
from .views import *
urlpatterns = [
    url('index/', Index.as_view(), name='index'),
    url('list/(\d+)/1/', ProductListView.as_view(), name='index'),
    # url(r'^list/(\d+)/1/$', ProductListView.as_view(), name='list'),
    # url(r'detail/(\d+)/$', ProductDetailView.as_view(), name='product_detail'),
    # url(r'^/create/$',Publish.Create_pub)
]