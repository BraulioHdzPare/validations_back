from django.contrib import admin
from apps.parking_sites.models import ParkingSite

# Register your models here.
@admin.register(ParkingSite)
class ParkingSiteAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "integration",
        "is_active",
        "updated_at",
    )

    list_filter = ("is_active", "integration_system_type")
    search_fields = ("code", "name")