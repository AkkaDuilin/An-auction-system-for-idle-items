from django.conf.urls import url
from .views import *
urlpatterns = [
    # url(r'^/auction/(?P<auction_id>\d+)/$', AuctionDetail.as_view(), name='auction-detail'),
    # url(r'^/auction/(?P<auction_id>\d+)/bid/$',AuctionBid.as_view(),name='auction-bid'),
    # url(r'^/auction/(?P<auction_id>\d+)/deposit/$',AuctionDepositPayment.as_view(),name='auction-deposit'),
    url('manage/',AuctionManage.detiel,name='auction-detiel'),
    url('create/',AuctionManage.create,name='auction-create'),
    url('auctions/<int:auction_id>/delete/', AuctionDelete.as_view(), name='auction_delete'),
    url('auctions/<int:auction_id>/update/', AuctionUpdate.as_view(), name='auction_update'),
    url('auctions/<int:auction_id>/', AuctionDetail.as_view(), name='auction_detail'),
]