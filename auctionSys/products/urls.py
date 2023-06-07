from django.conf.urls import url
from .views import *
urlpatterns = [
    url('', Index.as_view(), name='index'),
    url('list/<int:type_id>/<int:page>/<str:sort>/', ProductListView.as_view(), name='product_list'),
    url('detail/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    # url(r'^/create/$',Publish.Create_pub)
]