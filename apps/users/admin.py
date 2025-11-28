from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ("role", "country")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("role", "country")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Custom Fields", {"fields": ("role", "country")}),
    )
    list_filter = BaseUserAdmin.list_filter + ("role", "country")
    search_fields = ("username", "email", "country")
