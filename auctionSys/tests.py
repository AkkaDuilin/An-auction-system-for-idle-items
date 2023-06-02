from user_part.models import UserInfo
from products.models import ProductInfo, ProductType
from order.models import OrderInfo, OrderDetailInfo
from auctions.models import AuctionInfo,Bidder,BidderList
from django.db.models import Count
from collections import Counter
from datetime import timedelta
from django.utils import timezone


def create_users():
    # 创建用户1
    user1 = UserInfo.objects.create(
        user_name='user1',
        user_pwd='123456',
        user_email='user1@example.com',
        user_rman='User 1',
        user_address='Address 1',
        user_mnumber='123456',
        user_pnumber='123456789'
    )
    print(f"Created user 1 with ID: {user1.id}")

    # 创建用户2
    user2 = UserInfo.objects.create(
        user_name='user2',
        user_pwd='123456',
        user_email='user2@example.com',
        user_rman='User 2',
        user_address='Address 2',
        user_mnumber='654321',
        user_pnumber='987654321'
    )
    print(f"Created user 2 with ID: {user2.id}")

    # 创建用户3
    user3 = UserInfo.objects.create(
        user_name='user3',
        user_pwd='password3',
        user_email='user3@example.com',
        user_rman='User 3',
        user_address='Address 3',
        user_mnumber='111111',
        user_pnumber='222222222'
    )
    print(f"Created user 3 with ID: {user3.id}")



def test_output_UserInfo():
    users = UserInfo.objects.all()
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
    duplicates = UserInfo.objects.values('user_name').annotate(count=Count('user_name')).filter(count__gt=1)

    # 删除重复项
    for duplicate in duplicates:
        users_to_delete = UserInfo.objects.filter(user_name=duplicate['user_name'])
        users_to_delete.exclude(id=users_to_delete.first().id).delete()

def find_user():
   
    user = UserInfo.objects.get(user_name=user_name)
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



def create_test_products():
    # 创建六种类型数据
    type_names = ['书籍', '交通工具', '电子设备', '电子外设', '本地拍品', '其他']
    for type_name in type_names:
        ProductType.objects.create(type_name=type_name)

    # 创建十个产品信息
    products_data = [
        {
            'product_name': '产品1',
            'product_img': '',
            'product_price': 9.99,
            'product_unit': '个',
            'product_abstract': '产品1摘要',
            'product_content': '<p>产品1内容</p>',
            'product_type_id': 1,
        },
        {
            'product_name': '产品2',
            'product_img': '',
            'product_price': 19.99,
            'product_unit': '个',
            'product_abstract': '产品2摘要',
            'product_content': '<p>产品2内容</p>',
            'product_type_id': 1,
        },
        {
            'product_name': '产品3',
            'product_img': '',
            'product_price': 29.99,
            'product_unit': '个',
            'product_abstract': '产品3摘要',
            'product_content': '<p>产品3内容</p>',
            'product_type_id': 2,
        },
        {
            'product_name': '产品4',
            'product_img': '',
            'product_price': 39.99,
            'product_unit': '个',
            'product_abstract': '产品4摘要',
            'product_content': '<p>产品4内容</p>',
            'product_type_id': 2,
        },
        {
            'product_name': '产品5',
            'product_img': '',
            'product_price': 49.99,
            'product_unit': '个',
            'product_abstract': '产品5摘要',
            'product_content': '<p>产品5内容</p>',
            'product_type_id': 3,
        },
        {
            'product_name': '产品6',
            'product_img': '',
            'product_price': 59.99,
            'product_unit': '个',
            'product_abstract': '产品6摘要',
            'product_content': '<p>产品6内容</p>',
            'product_type_id': 3,
        },
        {
            'product_name': '产品7',
            'product_img': '',
            'product_price': 69.99,
            'product_unit': '个',
            'product_abstract': '产品7摘要',
            'product_content': '<p>产品7内容</p>',
            'product_type_id': 4,
        },
        {
            'product_name': '产品8',
            'product_img': '',
            'product_price': 79.99,
            'product_unit': '个',
            'product_abstract': '产品8摘要',
            'product_content': '<p>产品8内容</p>',
            'product_type_id': 4,
        },
        {
            'product_name': '产品9',
            'product_img': '',
            'product_price': 89.99,
            'product_unit': '个',
            'product_abstract': '产品9摘要',
            'product_content': '<p>产品9内容</p>',
            'product_type_id': 5,
        },
        {
            'product_name': '产品10',
            'product_img': '',
            'product_price': 99.99,
            'product_unit': '个',
            'product_abstract': '产品10摘要',
            'product_content': '<p>产品10内容</p>',
            'product_type_id': 5,
        },
    ]

    for product_data in products_data:
        ProductInfo.objects.create(**product_data)

def create_test_auctions():
    user1 = UserInfo.objects.get(id=1)  # 假设存在ID为1的用户
    product1 = ProductInfo.objects.get(id=1)  # 假设存在ID为1的产品

    # 创建测试数据
    auction1 = AuctionInfo.objects.create(
        auction_id='A002',
        auction_seller=user1,
        auction_date=timezone.now(),
        auction_final_date=timezone.now()+timedelta(days=30),
        starting_price=100.00,
        description='Auction 1 Description',
        product=product1,
    )
    bidder1 = Bidder.objects.create(user=user1, bid_amount=150.00)
    bidder_list1 = BidderList.objects.create()
    bidder_list1.bidders.add(bidder1)
    auction1.bidder_list = bidder_list1
    auction1.current_bid = 150.00
    auction1.winning_bidder = bidder1
    auction1.save()

    
def print_auctions():
    # 获取所有的AuctionInfo对象
    auctions = AuctionInfo.objects.all()

    # 遍历每个对象并输出其内容
    for auction in auctions:
        print("Auction ID:", auction.auction_id)
        print("Auction Seller:", auction.auction_seller)
        print("Auction Date:", auction.auction_date)
        print("Auction Final Date:", auction.auction_final_date)
        print("Is Active:", auction.is_Active)
        print("Starting Price:", auction.starting_price)
        print("Description:", auction.description)
        print("Product:", auction.product)
        print("Current Bid:", auction.current_bid)
        print("Bid Count:", auction.bid_count)
        print("Winning Bidder:", auction.winning_bidder)
        
        print("--------------------")

def test_add_bidder():
    amount = 250.0
    user1 = UserInfo.objects.get(id=1)  
    product1 = ProductInfo.objects.get(id=1) 
    auction = AuctionInfo.objects.get(auction_id='A001')
    bidder1 = Bidder.objects.create(user=user1, bid_amount=amount)
    # bidder_list1 = BidderList.objects.create()
    # auction.bidder_list = bidder_list1
    bidder_list1 = auction.bidder_list
    bidder_list1.bidders.add(bidder1)
    auction.bidder_list = bidder_list1
    auction.winning_bidder = bidder1
    auction.current_bid = amount
    auction.bid_count += 1
    auction.save()
    # print(bidder_list1)
    print(auction.bidder_list)

def test_print_highest():
    user1 = UserInfo.objects.get(id=1)  
    product1 = ProductInfo.objects.get(id=1) 
    auction = AuctionInfo.objects.get(auction_id='A001')
    print(auction.bidder_list.get_highest_bidder())

# 运行测试
# create_users()
# delete_duplicate_users()
# test_output_UserInfo()
# test_user_creation()
# test_product_creation()
# find_products()
# test_order_creation()
# find_order()
# test_output_UserInfo()
# create_test_products()
# create_test_auctions()
print_auctions()
# test_add_bidder()
# test_print_highest()