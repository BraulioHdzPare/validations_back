from apps.integrations.base import IParkingProvider
from apps.integrations.dtos import TicketData, ValidationOptionData, ValidationResultData

class DesignaProvider(IParkingProvider):
    """Implemetación inicial para Designa.
    Por ahora es un placeholder. Despues aqui se conectara
    el consumo real de WebService/API"""

    def lookup_ticket(self, *, ticket_number:str, context:dict):
        return TicketData(
            ticket_number = ticket_number,
            status = "MOCKED",
            raw_response = {
                "provider": "DESIGNA",
                "message": "Respuesta simulada para lookup_ticket",
            }
        )
    
    def get_validation_options(self, *, ticket, context:dict):
        return [
            ValidationOptionData(
                code = "MOCK_DISCOUNT",
                name = "Descuento de prueba",
                description = "Validación simulada para desarrollo inicial get_validation_options",
            )
        ]
    
    def apply_validation(self, *, ticket_number:str, validation_code:str, context:dict):
        return ValidationResultData(
            success = True,
            message = f"Validación '{validation_code}' aplicada exitosamente al ticket '{ticket_number}' (simulado)",
            external_reference = "MOCK_REF_123456",
            raw_request = {
                "ticket_number": ticket_number,
                "validation_code": validation_code,
            },
            raw_response = {
                "provider": "DESIGNA",
                "status": "OK",
            },
        )

    def health_check(self):
        return {"provider": "DESIGNA", "status": "OK"}