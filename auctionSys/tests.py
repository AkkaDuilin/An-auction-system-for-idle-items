from user_part.models import Userinfo
from products.models import ProductInfo, ProductType
from order.models import OrderInfo
from django.db.models import Count
from collections import Counter

def test_output_userinfo():
    users = Userinfo.objects.all()
    for user in users:
        print(f"User ID: {user.id}")
        print(f"Username: {user.user_name}")
        print(f"Password: {user.user_pwd}")
        print(f"Email: {user.user_email}")
        print(f"Real Name: {user.user_rman}")
        print(f"Address: {user.user_address}")
        print(f"Mobile Number: {user.user_mnumber}")
        print(f"Phone Number: {user.user_pnumber}")
        print("------------")

def delete_duplicate_users():
    # 获取重复项的用户名和数量
    duplicates = Userinfo.objects.values('user_name').annotate(count=Count('user_name')).filter(count__gt=1)

    # 删除重复项
    for duplicate in duplicates:
        users_to_delete = Userinfo.objects.filter(user_name=duplicate['user_name'])
        users_to_delete.exclude(id=users_to_delete.first().id).delete()

def find_user():
   
    user = Userinfo.objects.get(user_name=user_name)
    if user:
        print(f"User ID: {user.id}")
        print(f"Username: {user.user_name}")
        print(f"Password: {user.user_pwd}")
        print(f"Email: {user.user_email}")
        print(f"Real Name: {user.user_rman}")
        print(f"Address: {user.user_address}")
        print(f"Mobile Number: {user.user_mnumber}")
        print(f"Phone Number: {user.user_pnumber}")
        print("------------")

def find_products():
    all_products = ProductInfo.objects.all()
    for product in all_products:
        print(f"Product: {product.product_name}")

def find_order():
    all_order = OrderInfo.objects.all()
    for order in all_order:
        print(f"order: {order.order_id}")


def test_user_creation():
    # 创建测试用户
    user = UserInfo.objects.create(user_name='Test User', user_pwd='password', user_email='test@example.com')

    # 验证用户是否成功创建
    assert user.user_name == 'Test User'
    assert user.user_email == 'test@example.com'

def test_product_creation():
    # 创建测试产品类型
    product_type = ProductType.objects.create(type_name='Test Type')

    # 创建测试产品
    product = ProductInfo.objects.create(
        product_name='Test Product',
        product_price=10.99,
        product_type=product_type,
        product_stock=10
    )

    # 验证产品是否成功创建
    assert product.product_name == 'Test Product'
    assert product.product_price == 10.99
    assert product.product_stock == 10

def test_order_creation():
    print(233)
    # 创建测试订单
    order = OrderInfo.objects.create(
        order_id='123456744',
        order_user= Userinfo.objects.get(user_name='dyl'),
        order_seller= Userinfo.objects.get(user_name='txs'),
        total_price=50.00,
        order_pro_id = ProductInfo.objects.get(product_name = 'Test Product'),
        address='Test Address'
    )



    assert order.order_id == '123456744'

    assert order.total_price == 50.00
    assert order.address == 'Test Address'
    print("create success")
    # 验证订单是否成功创建


# 运行测试
# delete_duplicate_users()
# test_output_userinfo()
#test_user_creation()
#test_product_creation()
# find_products()
test_order_creation()

# find_order()

