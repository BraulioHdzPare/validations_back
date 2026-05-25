from django.apps import AppConfig


class IntegrationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.integrations'
    verbose_name = 'Integraciones'

    def ready(self):
        # Importar las señales para que se registren
        from apps.integrations.registry import provider_registry
        from apps.integrations.clients.designa.adapter import DesignaProvider

        provider_registry.register("DESIGNA", DesignaProvider)