from django.conf.urls import url
from .views import *
urlpatterns = [
    # url(r'^/auction/(?P<auction_id>\d+)/$', AuctionDetail.as_view(), name='auction-detail'),
    # url(r'^/auction/(?P<auction_id>\d+)/bid/$',AuctionBid.as_view(),name='auction-bid'),
    # url(r'^/auction/(?P<auction_id>\d+)/deposit/$',AuctionDepositPayment.as_view(),name='auction-deposit'),
    url('manage/',AuctionManage.detiel,name='auction-detiel'),
    url('create/',AuctionManage.create,name='auction-create'),
    url(r'delete(\d+)/$', AuctionDelete.delete, name='auction_delete'),
    url(r'^update(\d+)/$', AuctionUpdate.detail, name='auction_update'),
    url(r'^update(\d+)/update/$', AuctionUpdate.update, name='auction_update_handler'),
    url(r'(\d+)/$', AuctionDetail.detail, name='auction_detail'),
]