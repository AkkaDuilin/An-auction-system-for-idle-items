from user_part.models import Userinfo
from django.db.models import Count
from collections import Counter

def test_output_userinfo():
    print(23333)
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

def delete_duplicate_users(TestCase):
    # 获取重复项的用户名和数量
    duplicates = Userinfo.objects.values('user_name').annotate(count=Count('user_name')).filter(count__gt=1)

    # 删除重复项
    for duplicate in duplicates:
        users_to_delete = Userinfo.objects.filter(user_name=duplicate['user_name'])
        users_to_delete.exclude(id=users_to_delete.first().id).delete()


def UserinfoTestCase():
    user = Userinfo.objects.create(
        user_name='testuser',
        user_pwd='testpassword',
        user_email='testemail@test.com',
    )
    print(f'Created user: {user.user_name}, {user.user_email}')


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

#delete_duplicate_users()
#test_output_userinfo()
#UserinfoTestCase()