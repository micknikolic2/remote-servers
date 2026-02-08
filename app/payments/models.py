from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Entity class for table payments
class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    booking_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bookings.booking_id", ondelete="RESTRICT"),
        nullable=False,
    )

    hardware_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("machines.hardware_id", ondelete="RESTRICT"),
        nullable=False,
    )

    payer_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.customer_id", ondelete="RESTRICT"),
        nullable=False,
    )

    provider_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.customer_id", ondelete="SET NULL"),
        nullable=True,
    )

    amount_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False, server_default="EUR")
    payment_status: Mapped[str] = mapped_column(Text, nullable=False, server_default="incomplete")

    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    invoice_number: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    booking: Mapped["Booking"] = relationship("Booking", back_populates="payments")
    machine: Mapped["Machine"] = relationship("Machine", back_populates="payments")

    payer: Mapped["User"] = relationship(
        "User",
        back_populates="payments_as_payer",
        foreign_keys=[payer_id],
    )

    provider: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="payments_as_provider",
        foreign_keys=[provider_id],
    )

    __table_args__ = (
        CheckConstraint("amount_total >= 0", name="chk_payments_amount_non_negative"),
        CheckConstraint("payment_status IN ('incomplete', 'paid', 'failed')", name="chk_payment_status"),
        Index("idx_payments_booking_id", "booking_id"),
        Index("idx_payments_payer_id", "payer_id"),
        Index("idx_payments_provider_id", "provider_id"),
        Index("idx_payments_timestamp", "timestamp"),
        Index("idx_payments_status", "payment_status"),
    )