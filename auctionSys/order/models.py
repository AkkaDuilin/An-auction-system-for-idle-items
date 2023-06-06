from django.db import models


class OrderInfo(models.Model):
    ORDER_STATUS_CHOICES = (
        (0, '未付款'),
        (1, '已付款'),
        (2, '已发货'),
        (3, '已结束'),
    )
    order_id = models.CharField(max_length=20, primary_key=True)
    order_user = models.ForeignKey('user_part.UserInfo', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=0) 
    auction = models.ForeignKey('auctions.AuctionInfo', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.auction.current_bid
        super().save(*args, **kwargs)

    
