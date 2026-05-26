from django.contrib import admin
from apps.tenants.models import Tenant

# Register your models here.
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "trade_name",
        "is_active",
        "updated_at",
    )

    list_filter = ("is_active")
    search_fields = ("name", "trade_name")
    filter_horizontal = ("parking_sites",)
    