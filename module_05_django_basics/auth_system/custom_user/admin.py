from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["email", "username", "first_name", "is_verified", "is_staff"]
    list_filter = ["is_staff", "is_verified", "is_active"]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering = ["email"]

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("bio", "date_of_birth", "is_verified")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("email", "bio")}),
    )