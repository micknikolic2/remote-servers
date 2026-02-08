from __future__ import annotations

import uuid
from typing import Optional, List, Dict, Any

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Entity class for table machines
class Machine(Base):
    __tablename__ = "machines"

    hardware_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.customer_id", ondelete="RESTRICT"),
        nullable=False,
    )

    gpu_model: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cpu_model: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ram_gb: Mapped[int] = mapped_column(Integer, nullable=False)

    disk_type: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disk_size_gb: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    network_bandwidth: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    os: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    provider_agent_status: Mapped[str] = mapped_column(Text, nullable=False, server_default="offline")
    health_indicators: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    owner: Mapped["User"] = relationship("User", back_populates="machines")
    listings: Mapped[List["Listing"]] = relationship("Listing", back_populates="machine")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="machine")
    benchmarks: Mapped[List["Benchmark"]] = relationship("Benchmark", back_populates="machine")
    payments: Mapped[List["Payment"]] = relationship("Payment", back_populates="machine")
    metric_samples = relationship("MetricSample", back_populates="machine")

    __table_args__ = (
        CheckConstraint("ram_gb > 0", name="chk_machines_ram_positive"),
        CheckConstraint("disk_size_gb IS NULL OR disk_size_gb > 0", name="chk_machines_disk_positive"),
        CheckConstraint("provider_agent_status IN ('online', 'offline')", name="chk_provider_agent_status"),
        Index("idx_machines_customer_id", "customer_id"),
        Index("idx_machines_status", "provider_agent_status"),
    )
