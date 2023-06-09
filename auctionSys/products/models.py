from django.db import models
from tinymce.models import HTMLField





class ProductInfo(models.Model):
    TYPE_CHOICES = (
        (1, '书籍'),
        (2, '交通工具'),
        (3, '电子设备'),
        (4, '电子外设'),
        (5, '本地拍品'),
        (6, '其他'),
    )
    product_name = models.CharField(max_length=30)
    product_img = models.ImageField(upload_to='static/product_img/',max_length=100, blank=True, null=True, verbose_name='商品图片')
    product_price = models.DecimalField(max_digits=6, decimal_places=2)
    is_Delete = models.BooleanField(default=False)
    product_click = models.IntegerField(default=0)
    # product_unit = models.CharField(max_length=20)
    product_abstract = models.CharField(max_length=120)
    product_content = HTMLField()
    product_type = models.IntegerField(choices=TYPE_CHOICES)

    def __str__(self):
        return f"Bidder List: {self.id} -  {self.product_name}"


