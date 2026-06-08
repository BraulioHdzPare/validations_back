from django.conf import settings
from django.db import models

# Create your models here.
class ValidationType(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    external_code = models.CharField(max_length=100)

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    parking_sites = models.ManyToManyField(
        "parking_sites.ParkingSite",
        related_name = "validation_types",
        blank = True,
    )

    tenants = models.ManyToManyField(
        "tenants.Tenant",
        related_name = "validation_types",
        blank = True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tipo de Validacion"
        verbose_name_plural = "Tipos de Validacion"

    def __str__(self):
        return self.name
    

class ValidationLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="validation_logs",
    )

    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.PROTECT,
        related_name="validation_logs",
        null=True,
        blank=True,
    )

    parking_site = models.ForeignKey(
        "parking_sites.ParkingSite",
        on_delete=models.PROTECT,
        related_name="validation_logs",
    )

    validation_type = models.ForeignKey(
        "validations.ValidationType",
        on_delete=models.PROTECT,
        related_name="logs",
    )

    ticket_number = models.CharField(max_length=100)

    original_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    external_system = models.CharField(max_length=50)
    external_reference = models.CharField(max_length=150, blank=True)
    external_status = models.CharField(max_length=50, blank=True)

    request_payload = models.JSONField(default=dict, blank=True)
    response_payload = models.JSONField(default=dict, blank=True)

    was_successful = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de Validacion"
        verbose_name_plural = "Logs de Validacion"

        indexes = [
            models.Index(fields=["ticket_number"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["parking_site", "created_at"]),
        ]

    def __str__(self):
        return f"{self.ticket_number} - {self.parking_site} - {self.created_at}"