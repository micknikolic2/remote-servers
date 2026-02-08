from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Entity class for table bookings
class Booking(Base):
    __tablename__ = "bookings"

    booking_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    listing_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("listings.listing_id", ondelete="RESTRICT"),
        nullable=False,
    )

    hardware_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("machines.hardware_id", ondelete="RESTRICT"),
        nullable=False,
    )

    buyer_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.customer_id", ondelete="RESTRICT"),
        nullable=False,
    )

    start_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    booking_status: Mapped[str] = mapped_column(Text, nullable=False, server_default="pending")

    listing: Mapped["Listing"] = relationship("Listing", back_populates="bookings")
    machine: Mapped["Machine"] = relationship("Machine", back_populates="bookings")
    buyer: Mapped["User"] = relationship("User", back_populates="bookings_as_buyer")
    invoice = relationship("Invoice", back_populates="booking", uselist=False)

    payments: Mapped[List["Payment"]] = relationship("Payment", back_populates="booking")

    __table_args__ = (
        CheckConstraint(
            "booking_status IN ('pending', 'active', 'completed', 'canceled', 'disputed')",
            name="chk_booking_status",
        ),
        CheckConstraint("end_timestamp > start_timestamp", name="chk_booking_times"),
        Index("idx_bookings_listing_id", "listing_id"),
        Index("idx_bookings_hardware_id", "hardware_id"),
        Index("idx_bookings_buyer_id", "buyer_id"),
        Index("idx_bookings_status", "booking_status"),
        Index("idx_bookings_start_end", "start_timestamp", "end_timestamp"),
    )
