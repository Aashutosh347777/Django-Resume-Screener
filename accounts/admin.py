# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  #from django db models

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    # Correct structure for editing existing users
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'profile_pictures', 'bio')}),
    )

    # Correct structure for adding new users
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'profile_pictures', 'bio')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)