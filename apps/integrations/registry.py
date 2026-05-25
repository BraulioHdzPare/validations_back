from apps.integrations.exceptions import ProviderNotRegisteredException

class ProviderRegistry:
    def __init__(self):
        self._providers = {}

    def register(self, system_type: str, provider_class):
        """Registra un nuevo proveedor de estacionamiento.
        system_type: Un identificador único para el tipo de sistema de estacionamiento.
        provider_class: La clase que implementa la interfaz IParkingProvider para este tipo de sistema.
        """
        self._providers[system_type] = provider_class

    def get(self,  system_type: str, *, config):
        provider_class = self._providers.get(system_type)

        if not provider_class:
            raise ProviderNotRegisteredException(f"No se ha registrado ningún proveedor para el tipo de sistema '{system_type}'")
        
        return provider_class(config=config)
    
provider_registry = ProviderRegistry()