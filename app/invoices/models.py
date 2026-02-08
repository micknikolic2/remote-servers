from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Entity class for table invoices
class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    booking_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bookings.booking_id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )

    payer_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.customer_id", ondelete="RESTRICT"),
        nullable=False,
    )

    provider_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.customer_id", ondelete="RESTRICT"),
        nullable=False,
    )

    amount_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False, server_default="EUR")

    status: Mapped[str] = mapped_column(Text, nullable=False, server_default="draft")
    issued_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    invoice_number: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    booking: Mapped["Booking"] = relationship("Booking", back_populates="invoice")
    payer: Mapped["User"] = relationship("User", foreign_keys=[payer_id])
    provider: Mapped["User"] = relationship("User", foreign_keys=[provider_id])

    __table_args__ = (
        CheckConstraint("amount_total >= 0", name="chk_invoices_amount_non_negative"),
        CheckConstraint("status IN ('draft','issued','paid','void')", name="chk_invoice_status"),
        Index("idx_invoices_booking_id", "booking_id"),
        Index("idx_invoices_payer_id", "payer_id"),
        Index("idx_invoices_provider_id", "provider_id"),
        Index("idx_invoices_created_at", "created_at"),
        Index("idx_invoices_status", "status"),
    )
