from django.contrib import admin
from apps.integrations.models import IntegrationConfig

# Register your models here.
@admin.register(IntegrationConfig)
class IntegrationConfigAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "system_type",
        "base_url",
        "auth_type",
        "is_active",
        "updated_at",
    )

    list_filter = ("system_type", "auth_type", "is_active")
    search_fields = ("name", "base_url", "username")
    readonly_fields = ("created_at", "updated_at")