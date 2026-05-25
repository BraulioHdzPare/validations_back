from abc import ABC, abstractmethod


class IParkingProvider(ABC):
    """
    Interfaz base que todos los sistemas de estacionamiento deben implementar para integrarse con nuestro sistema de validaciones.
    """

    def __init__(self, *, config):
        """
        Inicializa el proveedor de estacionamiento con la configuración necesaria.
        config: Un diccionario con la configuración específica del proveedor.
        """
        self.config = config

    @abstractmethod
    def lookup_ticket(self, *, ticket_number:str, context:dict):
        """Busca la información de un ticket de estacionamiento dado su número. 
        ticket_number: El número del ticket a buscar.
        context: Un diccionario con información adicional que pueda ser útil para la búsqueda
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_validations_options(self, *, ticket, context: dict):
        """Obtiene las opciones de validación disponibles para este proveedor.
        ticket: La información del ticket para el cual se quieren obtener las opciones de validación.
        context: Un diccionario con información adicional que pueda ser útil para determinar las opciones de validación
        """
        raise NotImplementedError
    
    @abstractmethod
    def apply_validation(self, *, ticket_number:str,validation_code:str,context:dict):
        """Aplica una validación a un ticket de estacionamiento.
        ticket_number: El número del ticket al que se le aplicará la validación.
        validation_code: El código de la validación a aplicar.
        context: Un diccionario con información adicional que pueda ser útil para aplicar la validación
        """
        raise NotImplementedError
    
    @abstractmethod
    def health_check(self):
        """Realiza una verificación de salud para asegurarse de que el proveedor esté funcionando correctamente."""
        raise NotImplementedError