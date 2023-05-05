# 在 Django shell 中导入模型
from products.models import ProductType, ProductInfo

# 创建一个产品类型对象
type1 = ProductType.objects.create(type_name='电子产品')

# 创建一个产品对象，并关联到产品类型
product1 = ProductInfo.objects.create(
    product_name='iPhone 12', 
    product_price=6999, 
    product_click=100, 
    product_unit='台', 
    product_abstract='苹果的最新款手机', 
    product_stock=50, 
    product_content='<p>这是 iPhone 12 的详细介绍</p>', 
    product_type=type1
)

# 打印创建的产品对象
print(product1)

