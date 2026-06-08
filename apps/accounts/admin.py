from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "role", "tenant", "is_active", "date_joined")
    list_filter = ("role", "is_active", "tenant")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Rol y acceso",
            {
                "fields": ("role", "tenant", "parking_sites"),
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Rol y acceso",
            {
                "fields": ("role", "tenant", "parking_sites"),
            },
        ),
    )
