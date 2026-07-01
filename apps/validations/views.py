from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from apps.validations.serializers import (
    TicketLookupRequestSerializer,
    ApplyValidationRequestSerializer
)
from apps.validations.services import (
    TicketLookupService,
    ApplyValidationService
)
from apps.integrations.exceptions import IntegrationError, TicketNotFoundError


class TicketLookupAPIView(APIView):
    """API para consultar un ticket y sus opciones de validación."""

    def post(self, request):
        serializer = TicketLookupRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = TicketLookupService().execute(
                user = request.user,
                parking_site_id = serializer.validated_data['parking_site_id'],
                ticket_number = serializer.validated_data['ticket_number']
            )
        except TicketNotFoundError:
            return Response(
                {"ticket": None, "validation_options": []},
                status=status.HTTP_200_OK,
            )
        except IntegrationError as exc:
            return Response(
                {"detail": f"Error de integración: {exc}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        ticket = result['ticket']
        options = result['validation_options']

        return Response(
            {
                "ticket": {
                    "ticket_number": ticket.ticket_number,
                    "status": ticket.status,
                    "entry_datetime": ticket.entry_datetime,
                    "current_amount": ticket.current_amount,
                    "paid_amount": ticket.paid_amount,
                    "currency": ticket.currency,
                },
                "validation_options": [
                    {
                    "code": option.code,
                    "name": option.name,
                    "description": option.description
                    }
                    for option in options
                ],
            },
            status=status.HTTP_200_OK,
        )
    

class ApplyValidationAPIView(APIView):
    """API para aplicar una validación a un ticket."""
    
    def post(self, request):
        serializer = ApplyValidationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = ApplyValidationService().execute(
            user = request.user,
            parking_site_id = serializer.validated_data['parking_site_id'],
            ticket_number = serializer.validated_data['ticket_number'],
            validation_code = serializer.validated_data['validation_code']
        )

        return Response(
            {
                "success": result.success,
                "message": result.message,
                "external_reference": result.external_reference,
                "original_amount": result.original_amount,
                "final_amount": result.final_amount,
            },
            status=status.HTTP_200_OK if result.success else status.HTTP_400_BAD_REQUEST,
        )