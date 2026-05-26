from django.shortcuts import render
from requests import options
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


class TicketLookupAPIView(APIView):
    """API para consultar un ticket y sus opciones de validación."""

    def post(self, request):
        serializer = TicketLookupRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = TicketLookupService().execute(
            user = request.user,
            parking_site_id = serializer.validated_data['parking_site_id'],
            ticket_number = serializer.validated_data['ticket_number']
        )

        ticket = result['ticket']
        option = result['validation_options']

        return Response(
            {
                "ticket": {
                    "ticket_number": ticket.ticket_number,
                    "status": ticket.status,
                    "entry_time": ticket.entry_datetime,
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
            validation_type_id = serializer.validated_data['validation_type_id']
        )

        return Response(
            {
                "success": result.success,
                "message":result.message,
                "external_reference": result.external_reference,
            },
            status=status.HTTP_200_OK if result.success else status.HTTP_400_BAD_REQUEST,
        )