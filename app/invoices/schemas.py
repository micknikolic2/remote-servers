
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

# API schema models for invoice endpoints
# These models define the external API contract
class InvoiceCreate(BaseModel):
    booking_id: UUID
    payer_id: UUID
    provider_id: UUID
    amount_total: Decimal = Field(..., ge=0)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    notes: Optional[str] = None

class InvoiceRead(BaseModel):
    invoice_id: UUID
    booking_id: UUID
    payer_id: UUID
    provider_id: UUID
    amount_total: Decimal
    currency: str
    status: str
    invoice_number: str
    issued_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    created_at: datetime
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
