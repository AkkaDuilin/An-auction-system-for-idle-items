from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^/auction/(?P<auction_id>\d+)/$', AuctionDetail.as_view(), name='auction-detail'),
    url(r'^/auction/(?P<auction_id>\d+)/bid/$',AuctionBid.as_view(),name='auction-bid'),
    url(r'^/create/$',AuctionCreate.as_view(),name='auction-create')
]