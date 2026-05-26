from django.db import models

# Create your models here.
class ParkingSite(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    integration = models.ForeignKey(
        "integrations.IntegrationConfig",
        on_delete = models.PROTECT,
        related_name = "parking_sites",
    )

    address = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"

    def __str__(self):
        return f"{self.name} - ({self.code})"