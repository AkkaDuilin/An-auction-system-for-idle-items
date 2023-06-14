from django.conf.urls import url
from .views import *
urlpatterns = [
    # url(r'^/auction/(?P<auction_id>\d+)/$', AuctionDetail.as_view(), name='auction-detail'),
    # url(r'^/auction/(?P<auction_id>\d+)/bid/$',AuctionBid.as_view(),name='auction-bid'),
    # url(r'^/auction/(?P<auction_id>\d+)/deposit/$',AuctionDepositPayment.as_view(),name='auction-deposit'),
    url('manage/',AuctionManage.detail,name='auction-detail'),
    url('create/',AuctionManage.create,name='auction-create'),
    url(r'delete(\d+)/$', AuctionDelete.delete, name='auction_delete'),
    url(r'^update(\d+)/$', AuctionUpdate.detail, name='auction_update'),
    url(r'^update(\d+)/update/$', AuctionUpdate.update, name='auction_update_handler'),
    url(r'(\d+)/$', AuctionDetail.detail, name='auction_detail'),
    url(r'(\d+)/deposit/$', AuctionDepositPayment.deposit, name='auction_deposit'),
    url(r'(\d+)/reserve/$', Auctionreserve.reserve, name='auction_reserve'),
    url(r'(\d+)/bid/$', AuctionBid.bid, name='auction_bid'),
    url(r'reserve/$', AuctionreserveDetail.detail, name='auction_reserve'),
]