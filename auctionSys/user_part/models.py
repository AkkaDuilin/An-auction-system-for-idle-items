from django.db import models
from itsdangerous import TimedSerializer  as Serializer
from django.conf import settings as d_set
from django.contrib.auth.models import AbstractUser

SECRET_KEY = d_set.SECRET_KEY


# class UserInfo(AbstractUser):
#     user_rman = models.CharField(max_length=20, default='')
#     user_address = models.CharField(max_length=100, default='')
#     user_mnumber = models.CharField(max_length=6, default='')
#     user_pnumber = models.CharField(max_length=11, default='')
#     deposit_balance = models.IntegerField(default=0)


#     def generate_reset_token(self, expiration=3600):
#         s = Serializer(SECRET_KEY, expiration)
#         return s.dumps({'reset': self.id}).decode('utf-8')

#     @staticmethod
#     def reset_password(token, new_password):
#         s = Serializer(d_set.SECRET_KEY)
#         try:
#             data = s.loads(token.encode('utf-8'))
#         except:
#             return False
#         user = UserInfo.objects.filter(id=data.get('reset')).first()
#         if not user:
#             return False
#         user.user_pwd = new_password
#         user.save()
#         return True


class UserInfo(models.Model):
    user_name = models.CharField(max_length=20)
    user_pwd = models.CharField(max_length=40)
    user_email = models.CharField(max_length=40)
    user_rman = models.CharField(max_length=20, default='')
    user_address = models.CharField(max_length=100, default='')
    user_mnumber = models.CharField(max_length=6, default='')
    user_pnumber = models.CharField(max_length=11, default='')
    deposit_balance = models.IntegerField(default=0)
    last_login = models.DateTimeField(auto_now_add=True)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(SECRET_KEY, expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(d_set.SECRET_KEY)
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = UserInfo.objects.filter(id=data.get('reset')).first()
        if not user:
            return False
        user.user_pwd = new_password
        user.save()
        return True
