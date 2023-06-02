from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^/auction/(?P<auction_id>\d+)/$', AuctionDetail.as_view(), name='auction-detail'),
    url(r'^/create/auctions_create',AuctionCreate.as_view())
]