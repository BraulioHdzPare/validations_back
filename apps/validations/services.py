from apps.integrations.dispatcher import IntegrationDispatcher
from apps.parking_sites.models import ParkingSite
from apps.validations.models import ValidationType, ValidationLog


class TicketLookupService:
    """Servicio para manejar las consultas de tickets y opciones de validación."""

    def execute(self, *, user, parking_site_id: int, ticket_number: str):
        parking_site = ParkingSite.objects.select_related('integration').get(
            id=parking_site_id,
            is_active=True
        )

        dispatcher = IntegrationDispatcher(
            integration_config = parking_site.integration
        )

        ticket = dispatcher.lookup_ticket(
            ticket_number = ticket_number,
            context = {
                "user": user,
                "parking_site": parking_site,
            }
        )

        options = dispatcher.get_validation_options(
            ticket = ticket,
            context = {
                "user": user,
                "parking_site": parking_site,
            }
        )

        return {
            "ticket": ticket,
            "validation_options": options,
        }
    
class ApplyValidationService:
    """Servicio para aplicar una validación a un ticket."""
    
    def execute(
        self, *, user,
        parking_site_id: int,
        ticket_number: str,
        validation_type_id: int
    ):
        parking_site = ParkingSite.objects.select_related('integration').get(
            id=parking_site_id,
            is_active=True
        )

        validation_type = ValidationType.objects.get(
            id=validation_type_id,
            parking_site=parking_site
        )

        dispatcher = IntegrationDispatcher(
            integration_config = parking_site.integration
        )

        result = dispatcher.apply_validation(
            ticket_number = ticket_number,
            validation_code = validation_type.external_code,
            context = {
                "user": user,
                "parking_site": parking_site,
                "validation_type": validation_type,
            }
        )

        ValidationLog.objects.create(
            user = user,
            parking_site = parking_site,
            ticket_number = ticket_number,
            validation_type = validation_type,
            external_system = parking_site.integration.system_type,
            external_reference = result.external_reference or "",
            external_status = "OK" if result.success else "FAILED",
            request_payload = result.raw_request or {},
            response_payload = result.raw_response or {},
            was_successful = result.success,
            error_message = "" if result.success else result.message,
        )

        return result