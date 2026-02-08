
from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional

# API contract models (DTOs) for listing endpoints
class ListingCreate(BaseModel):
    hardware_id: UUID

    price_hour: Optional[Decimal] = Field(default=None, ge=0)
    price_day: Optional[Decimal] = Field(default=None, ge=0)
    price_week: Optional[Decimal] = Field(default=None, ge=0)

    currency: str = Field(default="EUR", min_length=3, max_length=3)
    status: str = Field(default="active", pattern="^(active|paused|archived)$")


class ListingRead(BaseModel):
    listing_id: UUID
    hardware_id: UUID

    price_hour: Optional[Decimal] = None
    price_day: Optional[Decimal] = None
    price_week: Optional[Decimal] = None

    currency: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
