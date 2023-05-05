from django.test import TestCase
from user_part.models import Userinfo

class UserinfoTestCase(TestCase):
    def setUp(self):
        self.user = Userinfo.objects.create(
            user_name='testuser',
            user_pwd='testpassword',
            user_email='testemail@test.com',
        )
        print(f'Created user: {self.user.user_name}, {self.user.user_email}')

    # def test_reset_password(self):
    #     # Generate reset token
    #     token = self.user.generate_reset_token()
    #     print(token)
    #     # Reset password with token
    #     new_password = 'newpassword'
    #     result = Userinfo.reset_password(token, new_password)
    #     print(result)

    #     # Check if password was reset successfully
    #     self.assertTrue(result)

    #     # Check if new password is saved in database
    #     user = Userinfo.objects.get(id=self.user.id)
    #     self.assertEqual(user.user_pwd, new_password)


