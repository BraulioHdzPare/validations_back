from apps.integrations.base import IParkingProvider
from apps.integrations.clients.datapark.client import DataparkClient
from apps.integrations.clients.datapark.mappers import card_response_to_ticket
from apps.integrations.exceptions import InvalidExternalResponseError, TicketNotFoundError

# Códigos de resultado de QueryCardEntry (tabla 1.5 de la doc Web Validations).
RESULT_OK = 0
RESULT_DISCOUNT_ALREADY_APPLIED = 1
RESULT_NOT_REGISTERED = 2


class DataparkProvider(IParkingProvider):
    """Proveedor para la interfaz Web Validations de Datapark (DpWebService)."""

    def _client(self) -> DataparkClient:
        return DataparkClient.from_config(self.config)

    def lookup_ticket(self, *, ticket_number: str, context: dict):
        response = self._client().query_card_entry(
            card_number=ticket_number,
            calculate_amount=True,
        )

        result_code = int(response.ResultCode)
        if result_code == RESULT_NOT_REGISTERED:
            raise TicketNotFoundError(f"Boleto '{ticket_number}' no registrado en Datapark.")
        if result_code not in (RESULT_OK, RESULT_DISCOUNT_ALREADY_APPLIED):
            raise InvalidExternalResponseError(
                f"Datapark devolvió ResultCode={result_code} al consultar el boleto."
            )

        return card_response_to_ticket(response, requested_number=ticket_number)

    def get_validation_options(self, *, ticket, context: dict):
        # Bajo el contrato catálogo-only, las opciones salen de ValidationType,
        # no del proveedor. (GetDiscounts se usaría solo para sincronizar el catálogo.)
        raise NotImplementedError

    def apply_validation(self, *, ticket_number: str, validation_code: str, context: dict):
        # Pendiente: ApplyDiscount (siguiente paso de la integración).
        raise NotImplementedError

    def health_check(self):
        return {"provider": "DATAPARK", "version": self._client().get_service_version()}
