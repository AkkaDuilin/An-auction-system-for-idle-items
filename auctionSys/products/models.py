from django.db import models
from tinymce.models import HTMLField


class ProductType(models.Model):
    TYPE_CHOICES = (
        (1, '书籍'),
        (2, '交通工具'),
        (3, '电子设备'),
        (4, '电子外设'),
        (5, '本地拍品'),
        (6, '其他'),
    )

    type_name = models.IntegerField(choices=TYPE_CHOICES)
    # 返回类型名称
    def get_type_name(self):
        for choice in self.TYPE_CHOICES:
            if choice[0] == self.type_name:
                return choice[1]
        return ''


class ProductInfo(models.Model):
    product_name = models.CharField(max_length=30)
    product_img = models.ImageField(upload_to='product_img')
    product_price = models.DecimalField(max_digits=6, decimal_places=2)
    is_Delete = models.BooleanField(default=False)
    product_click = models.IntegerField(default=0)
    product_unit = models.CharField(max_length=20)
    product_abstract = models.CharField(max_length=120)
    product_content = HTMLField()
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


