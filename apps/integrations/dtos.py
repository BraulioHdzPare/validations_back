from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any

@dataclass
class TicketData:
    ticket_number: str
    status: str
    entry_datetime: datetime | None = None
    current_amount: Decimal | None = None
    paid_amount: Decimal | None = None
    currency: str = 'MXN'
    raw_response: dict[str, Any] | None = None


@dataclass
class ValidationOptionData:
    code: str
    name: str
    description: str | None = None
    raw_data: dict[str, Any] | None = None


@dataclass
class ValidationResultData:
    success: bool
    message: str | None = None
    external_reference: str | None = None
    original_amount: Decimal | None = None
    final_amount: Decimal | None = None
    raw_request: dict[str, Any] | None = None
    raw_response: dict[str, Any] | None = None