from django.db import models

from apps.integrations.fields import EncryptedTextField

# Create your models here.
class IntegrationConfig(models.Model):
    SYSTEM_DESIGNA = "DESIGNA"
    SYSTEM_DATAPARK = "DATAPARK"
    SYSTEM_ZEAG = "ZEAG"
    SYSTEM_MEYPAR = "MEYPAR"

    SYSTEM_CHOICES = [
        (SYSTEM_DESIGNA, "Designa"),
        (SYSTEM_DATAPARK, "Datapark"),
        (SYSTEM_ZEAG, "Zeag"),
        (SYSTEM_MEYPAR, "Meypar"),
    ]

    AUTH_NONE = "NONE"
    AUTH_BASIC = "BASIC"
    AUTH_TOKEN = "TOKEN"

    AUTH_CHOICES = [
        (AUTH_NONE, "Sin autenticación"),
        (AUTH_BASIC, "Autenticación básica"),
        (AUTH_TOKEN, "Token de autenticación"),
    ]

    name = models.CharField(max_length=150) 
    system_type = models.CharField(max_length=50, choices=SYSTEM_CHOICES) # Identifica el tipo de sistema de estacionamiento (Designa, Datapark, etc.)
    base_url = models.URLField(blank = True) # Puede ser opcional si el proveedor no lo requiere o lo maneja internamente.
    auth_type = models.CharField(max_length=30, choices=AUTH_CHOICES, default=AUTH_NONE) # Define el tipo de autenticación que se usará para este proveedor. 
                                                                                         # Esto ayudará a la lógica de conexión a saber qué credenciales esperar y cómo usarlas.
                                                                                        
    username = models.CharField(max_length=150, blank=True)
    encrypted_password = EncryptedTextField(blank=True)
    encrypted_token = EncryptedTextField(blank=True)

    extra_config = models.JSONField(default=dict, blank=True)
    timeout_seconds = models.PositiveIntegerField(default=20)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración de Integracion"
        verbose_name_plural = "Configuraciones de Integracion"

    def __str__(self):
        return f"{self.name} ({self.system_type})"


class TenantIntegrationIdentity(models.Model):
    """Identidad de un locatario (Tenant) frente a un sistema de estacionamiento externo.

    Genérico a propósito: cada proveedor define qué identificadores necesita y los
    guarda en `identifiers` (JSON). Así un PARCS que NO use el concepto de 'merchant'
    simplemente no tiene fila aquí, sin afectar al dominio ni a otros proveedores.

    Ejemplos de `identifiers`:
        Datapark Web Validations -> {"merchant_key": "1", "merchant_id": "ACME"}
        Otro proveedor           -> {"cost_center": "CC-09"}  (o vacío, si no aplica)
    """

    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="integration_identities",
    )
    integration = models.ForeignKey(
        "integrations.IntegrationConfig",
        on_delete=models.CASCADE,
        related_name="tenant_identities",
    )

    # Identificadores que el proveedor concreto necesita para reconocer al locatario.
    identifiers = models.JSONField(default=dict, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Identidad de Locatario por Integración"
        verbose_name_plural = "Identidades de Locatario por Integración"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "integration"],
                name="uniq_tenant_integration_identity",
            )
        ]

    def __str__(self):
        return f"{self.tenant} @ {self.integration}"