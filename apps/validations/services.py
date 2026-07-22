from rest_framework.exceptions import NotFound

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

        # Catálogo local: las validaciones aplicables salen de los ValidationType
        # ligados a este parking_site, no del proveedor externo.
        options = ValidationType.objects.filter(
            parking_sites = parking_site,
            is_active = True,
        )
        if getattr(user, "is_tenant_user", False) and user.tenant_id:
            options = options.filter(tenants = user.tenant)

        return {
            "ticket": ticket,
            "validation_options": list(options),
        }
    
class ApplyValidationService:
    """Servicio para aplicar una validación a un ticket."""
    
    def execute(
        self, *, user,
        parking_site_id: int,
        ticket_number: str,
        validation_code: str
    ):
        parking_site = ParkingSite.objects.select_related('integration').get(
            id=parking_site_id,
            is_active=True
        )

        # Mismo filtrado que TicketLookupService: la validación debe estar activa
        # y ligada a esta unidad y —si el usuario es locatario— a su tenant.
        # Sin este filtro por tenant, un tenant_user podría aplicar un descuento
        # no autorizado para su locatario conociendo su `code`.
        candidates = ValidationType.objects.filter(
            code=validation_code,
            parking_sites=parking_site,
            is_active=True,
        )
        if getattr(user, "is_tenant_user", False) and user.tenant_id:
            candidates = candidates.filter(tenants=user.tenant)

        try:
            validation_type = candidates.get()
        except ValidationType.DoesNotExist:
            raise NotFound("La validación seleccionada no está disponible para esta unidad.")

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
            tenant = user.tenant,
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