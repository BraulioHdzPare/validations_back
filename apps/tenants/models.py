from django.db import models

# Create your models here.
class Tenant(models.Model):
    name = models.CharField(max_length=150)
    trade_name = models.CharField(max_length=150, blank=True)
    parking_sites = models.ManyToManyField(
        "parking_sites.ParkingSite",
        related_name = "tenants",
        blank = True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Locatario"
        verbose_name_plural = "Locatarios"

    def __str__(self):
        return self.name or self.trade_name