
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# API contract models (DTOs) for payment endpoints
class PaymentCreate(BaseModel):
    booking_id: UUID
    hardware_id: UUID

    payer_id: UUID
    provider_id: Optional[UUID] = None

    amount_total: Decimal = Field(..., ge=0)
    currency: str = Field(default="EUR", min_length=3, max_length=3)

    invoice_number: Optional[str] = None


class PaymentRead(BaseModel):
    payment_id: UUID
    booking_id: UUID
    hardware_id: UUID

    payer_id: UUID
    provider_id: Optional[UUID] = None

    amount_total: Decimal
    currency: str
    payment_status: str
    timestamp: datetime
    invoice_number: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CheckoutRequest(BaseModel):
    booking_id: UUID
    hardware_id: UUID
    amount: float
    currency: str = "EUR"
