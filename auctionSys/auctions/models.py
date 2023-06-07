from datetime import timedelta
from django.db import models
from user_part.models import UserInfo
from products.models import ProductInfo
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Bidder(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    if_pay_deposit = models.BooleanField(default=False)

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
    def get_bidders_count(self):
         
         return self.bidders.count()
    def get_all_bidders(self):
        return self.bidders.all()

    def __str__(self):
        if self.bidders:
            bidders_str = ', '.join(str(bidder) for bidder in self.bidders.all())
            return f"Bidder List: {bidders_str}"
        else:
            return "Bidder List: No bidders"

class AuctionInfo(models.Model):
    # 以下字段为拍卖信息
    auction_seller = models.ForeignKey(UserInfo, on_delete=models.CASCADE)  
    auction_date = models.DateTimeField()
    auction_final_date = models.DateTimeField()   
    AUCTION_STATUS_CHOICES = (
        (1, '未开始'),
        (2, '进行中'),
        (3, '结束'),
    )
    auction_status = models.IntegerField(choices=AUCTION_STATUS_CHOICES, default=1)
    starting_price = models.DecimalField(max_digits=8, decimal_places=2)
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    deposit_amount = models.DecimalField(max_digits=8, decimal_places=2,null=True) 
    # 以下字段为参加拍卖者列表信息 
    current_bid = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    winning_bidder = models.ForeignKey(Bidder, on_delete=models.CASCADE, null=True, blank=True)
    # bidder_list 可以使用两个方法获取最高出价者和出价者数量
    bidder_list = models.ForeignKey(BidderList, on_delete=models.CASCADE, null=True, blank=True)
    # 每次保存模型时，auction_final_date 将会被自动设置为 auction_date 加三个小时的时间。
    # bid_count = models.IntegerField(default=0)
    
    def get_auctions_by_product_ids(product_ids):
        auctions = AuctionInfo.objects.filter(products__id__in=product_ids).distinct()
        return auctions
    
    def save(self, *args, **kwargs):
        self.auction_final_date = self.auction_date + timedelta(days=3)
        
        # self.bid_count = self.bidder_list.get_bidders_count()
        super().save(*args, **kwargs)

@receiver(pre_save, sender=AuctionInfo)
def calculate_deposit_amount(sender, instance, **kwargs):
    instance.deposit_amount = float(instance.starting_price) * 0.1
    


