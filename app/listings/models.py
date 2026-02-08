from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Entity class for table listings
class Listing(Base):
    __tablename__ = "listings"

    listing_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    hardware_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("machines.hardware_id", ondelete="RESTRICT"),
        nullable=False,
    )

    price_hour: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    price_day: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    price_week: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)

    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False, server_default="EUR")
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default="active")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    machine: Mapped["Machine"] = relationship("Machine", back_populates="listings")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="listing")

    __table_args__ = (
        CheckConstraint("status IN ('active', 'paused', 'archived')", name="chk_listing_status"),
        CheckConstraint(
            "(price_hour IS NULL OR price_hour >= 0) AND "
            "(price_day  IS NULL OR price_day  >= 0) AND "
            "(price_week IS NULL OR price_week >= 0)",
            name="chk_listing_price_non_negative",
        ),
        Index("idx_listings_hardware_id", "hardware_id"),
        Index("idx_listings_status", "status"),
        Index("idx_listings_created_at", "created_at"),
    )

