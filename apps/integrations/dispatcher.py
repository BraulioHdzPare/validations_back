from apps.integrations.registry import provider_registry

class IntegrationDispatcher:
    """Recibe una configuración de integración y despacha las llamadas al proveedor correspondiente."""

    def __init__(self, *, integration_config):
        self.integration_config = integration_config
        self.provider = provider_registry.get(
            integration_config.system_type,
            config = integration_config,
        )
    
    def lookup_ticket(self, *, ticket_number:str, context:dict):
        return self.provider.lookup_ticket(
            ticket_number=ticket_number,
            context=context,
        )
    
    def get_validation_options(self, *, ticket, context:dict):
        return self.provider.get_validation_options(
            ticket=ticket,
            context=context,
        )
    
    def apply_validation(self, *, ticket_number:str,validation_code:str,context:dict):
        return self.provider.apply_validation(
            ticket_number=ticket_number,
            validation_code=validation_code,
            context=context,
        )
    
    def health_check(self):
        return self.provider.health_check()