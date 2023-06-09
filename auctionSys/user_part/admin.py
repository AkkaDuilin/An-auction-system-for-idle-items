from django.contrib import admin
from .models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_rman', 'user_address', 'user_mnumber', 'user_pnumber')
    search_fields = ('user_name', 'user_email', 'user_rman', 'user_address', 'user_mnumber', 'user_pnumber')
    list_filter = ('user_name', 'user_email', 'user_rman', 'user_address', 'user_mnumber', 'user_pnumber')


admin.site.register(UserInfo, UserInfoAdmin)
