from django.db import models

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
    encrypted_password = models.TextField(blank=True)
    encrypted_token = models.TextField(blank=True)

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