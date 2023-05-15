from user_part.models import Userinfo
from products.models import ProductInfo, ProductType
from order.models import OrderInfo, OrderDetailInfo
from django.db.models import Count
from collections import Counter


def create_users():
    # 创建用户1
    user1 = Userinfo.objects.create(
        user_name='user1',
        user_pwd='password1',
        user_email='user1@example.com',
        user_rman='User 1',
        user_address='Address 1',
        user_mnumber='123456',
        user_pnumber='123456789'
    )
    print(f"Created user 1 with ID: {user1.id}")

    # 创建用户2
    user2 = Userinfo.objects.create(
        user_name='user2',
        user_pwd='password2',
        user_email='user2@example.com',
        user_rman='User 2',
        user_address='Address 2',
        user_mnumber='654321',
        user_pnumber='987654321'
    )
    print(f"Created user 2 with ID: {user2.id}")

    # 创建用户3
    user3 = Userinfo.objects.create(
        user_name='user3',
        user_pwd='password3',
        user_email='user3@example.com',
        user_rman='User 3',
        user_address='Address 3',
        user_mnumber='111111',
        user_pnumber='222222222'
    )
    print(f"Created user 3 with ID: {user3.id}")



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
        print(f"Product: {product.id}")

def find_order():
    print(2333)
    all_order = OrderInfo.objects.all()
    for order in all_order:
        print(f"order: {order.order_id}")

    all_order = OrderDetailInfo.objects.all()
    for order in all_order:
        print(f"order: {order.order.order_id}")

def delete_mod(ModelName):
    records = ModelName.objects.all()
    records.delete()

def test_user_creation():
    # 创建测试用户
    user = UserInfo.objects.create(user_name='Test User', user_pwd='password', user_email='test@example.com')

    # 验证用户是否成功创建
    assert user.user_name == 'Test User'
    assert user.user_email == 'test@example.com'

def test_product_creation():
    print("create product")
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
    print("create order")
    # 创建测试订单
    order = OrderInfo.objects.create(
        order_id='123456756',
        order_user= Userinfo.objects.get(user_name='dyl'),
        total_price=50.00,
        address='Test Address'
    )

    order_detail = OrderDetailInfo.objects.create(
        products = ProductInfo.objects.get(id = 1),
        order = order,
        price = 20.0,
        count = 5,
        order_seller = Userinfo.objects.get(user_name='txs'),
    )


    assert order.order_id == '123456756'
    assert order.total_price == 50.00
    assert order.address == 'Test Address'
    print("create success")
    # 验证订单是否成功创建


# 运行测试
# create_users
# delete_duplicate_users()
# test_output_userinfo()
# test_user_creation()
# test_product_creation()
find_products()
# test_order_creation()
# find_order()
