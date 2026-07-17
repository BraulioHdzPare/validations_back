from django.contrib import admin
from apps.validations.models import ValidationType, ValidationLog

# Register your models here.
@admin.register(ValidationType)
class ValidationTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "external_code",
        "discount_type",
        "is_active",
        "updated_at",
    )

    list_filter = ("is_active", "discount_type")
    search_fields = ("name", "code", "external_code")
    filter_horizontal = ("parking_sites", "tenants")


@admin.register(ValidationLog)
class ValidationLogAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_number",
        "parking_site",
        "validation_type",
        "user",
        "was_successful",
        "created_at",
    )

    list_filter = ("was_successful", "validation_type", "parking_site", "created_at")
    search_fields = ("ticket_number", "external_reference", "user_name")
    readonly_fields = (
        "user",
        "tenant",
        "parking_site",
        "validation_type",
        "ticket_number",
        "original_amount",
        "final_amount",
        "external_system",
        "external_reference",
        "external_status",
        "request_payload",
        "response_payload",
        "was_successful",
        "error_message",
        "created_at",
    )
