from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador"
        TENANT_USER = "tenant_user", "Usuario Locatario"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TENANT_USER,
    )

    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    # Parking sites this user can operate (empty = all sites of their tenant)
    parking_sites = models.ManyToManyField(
        "parking_sites.ParkingSite",
        blank=True,
        related_name="users",
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    @property
    def is_admin(self) -> bool:
        return self.role == self.Role.ADMIN

    @property
    def is_tenant_user(self) -> bool:
        return self.role == self.Role.TENANT_USER

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"
