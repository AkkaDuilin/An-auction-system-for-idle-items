

from django.contrib import admin
from .models import Bidder, BidderList, AuctionInfo

admin.site.register(Bidder)
admin.site.register(BidderList)
admin.site.register(AuctionInfo)
