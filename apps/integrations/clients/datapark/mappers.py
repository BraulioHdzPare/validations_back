"""Mapea las respuestas de Datapark (zeep) a los DTOs del dominio."""
from datetime import datetime
from decimal import Decimal

from zeep.helpers import serialize_object

from apps.integrations.dtos import TicketData

# Datapark usa fechas centinela (año 1 o 1899) para representar "sin valor".
_MIN_REAL_YEAR = 1901


def _clean_datetime(value):
    if not isinstance(value, datetime) or value.year < _MIN_REAL_YEAR:
        return None
    return value


def _status_from_response(response) -> str:
    """Traduce el estado del boleto al vocabulario del portal (active/paid/expired/cancelled)."""
    if int(response.Paid or 0) == 1:
        return "paid"

    inlot = int(response.InlotStatus or 0)
    if inlot == 1:
        return "active"      # dentro del estacionamiento y no pagado -> validable
    if inlot == -1:
        return "expired"     # ya usó la salida del estacionamiento
    return "cancelled"       # estado desconocido / no validable


def card_response_to_ticket(response, *, requested_number: str) -> TicketData:
    """Convierte un CardResponseData (con ResultCode de éxito) en un TicketData.

    No decide el caso 'no encontrado'; eso lo evalúa el provider según ResultCode.
    """
    amount = None
    payment = response.PaymentInfo
    if payment is not None and payment.TotalAmountDue is not None:
        amount = Decimal(payment.TotalAmountDue)

    return TicketData(
        ticket_number=response.CardNumber or requested_number,
        status=_status_from_response(response),
        entry_datetime=_clean_datetime(response.EntryDateTime),
        current_amount=amount,
        paid_amount=None,
        currency="MXN",
        raw_response=serialize_object(response, dict),
    )
