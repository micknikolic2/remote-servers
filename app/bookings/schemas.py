
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime, timezone
from uuid import UUID
from enum import Enum

# API schema models for benchmark endpoints
# These models define the external API contract and DTO
class BookingStatus(str, Enum):
    pending = "pending"
    active = "active"
    completed = "completed"
    canceled = "canceled"
    disputed = "disputed"


class BookingRequest(BaseModel):
    listing_id: UUID
    start_timestamp: datetime
    end_timestamp: datetime

    @field_validator("start_timestamp", "end_timestamp", mode="after")
    @classmethod
    def ensure_timezone_aware(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class BookingAdminCreate(BookingRequest):
    buyer_id: UUID
    hardware_id: UUID


class BookingRead(BaseModel):
    booking_id: UUID
    listing_id: UUID
    hardware_id: UUID
    buyer_id: UUID
    start_timestamp: datetime
    end_timestamp: datetime
    created_at: datetime
    booking_status: str

    model_config = ConfigDict(from_attributes=True)
