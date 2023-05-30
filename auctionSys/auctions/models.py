from django.db import models
from user_part.models import UserInfo
from products.models import ProductInfo

class Bidder(models.Model):
    user = models.ForeignKey('user_part.UserInfo', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user.user_name} - {self.bid_amount}"

class BidderList(models.Model):
    bidders = models.ManyToManyField(Bidder)
    def get_highest_bidder(self):
        if self.bidders.exists():
            highest_bidder = self.bidders.order_by('-bid_amount').first()
            return highest_bidder
        else:
            return None

    def get_all_bidders(self):
        return self.bidders.all()

    def __str__(self):
        if self.bidders:
            bidders_str = ', '.join(str(bidder) for bidder in self.bidders.all())
            return f"Bidder List: {bidders_str}"
        else:
            return "Bidder List: No bidders"

class AuctionInfo(models.Model):
    auction_id = models.CharField(max_length=20, primary_key=True)
    auction_seller = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    auction_date = models.DateTimeField(auto_now=True)
    auction_final_date = models.DateTimeField()
    is_Active = models.BooleanField(default=True)
    starting_price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    current_bid = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    bid_count = models.IntegerField(default=0)
    winning_bidder = models.ForeignKey(Bidder, on_delete=models.CASCADE, null=True, blank=True)
    bidder_list = models.ForeignKey(BidderList, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.auction_id


