from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Entity class for table users
class User(Base):
    __tablename__ = "users"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    organization_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_billing_account: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    signup_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    machines: Mapped[List["Machine"]] = relationship("Machine", back_populates="owner")
    bookings_as_buyer: Mapped[List["Booking"]] = relationship("Booking", back_populates="buyer")
    verified_benchmarks: Mapped[List["Benchmark"]] = relationship("Benchmark", back_populates="verified_by_admin")

    payments_as_payer: Mapped[List["Payment"]] = relationship(
        "Payment",
        foreign_keys="Payment.payer_id",
        back_populates="payer",
    )
    payments_as_provider: Mapped[List["Payment"]] = relationship(
        "Payment",
        foreign_keys="Payment.provider_id",
        back_populates="provider",
    )


Index("idx_users_signup_date", User.signup_date)