class IntegrationError(Exception):
    """Clase base para errores relacionados con integraciones."""
    pass

class ProviderNotRegisteredError(IntegrationError):
    """El proveedor de estacionamiento no está registrado en el sistema."""

class ExternalServiceUnavailableError(IntegrationError):
    """El servicio externo del proveedor de estacionamiento no está disponible."""

class ExternalServiceTimeoutError(IntegrationError):
    """El servicio externo del proveedor de estacionamiento ha excedido el tiempo de espera."""

class InvalidExternalResponseError(IntegrationError):
    """La respuesta del servicio externo del proveedor de estacionamiento no es válida o no tiene el formato esperado."""

class TicketNotFoundError(IntegrationError):
    """No se encontró el ticket de estacionamiento en el sistema del proveedor."""

class ValidationRejectedError(IntegrationError):
    """La validación fue rechazada por el sistema del proveedor de estacionamiento."""

    