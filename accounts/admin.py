from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['id','email', 'username', 'first_name', 'last_name', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_superuser', 'is_active']