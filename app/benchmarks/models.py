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
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Entity class for table benchmarks
class Benchmark(Base):
    __tablename__ = "benchmarks"

    benchmark_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    hardware_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("machines.hardware_id", ondelete="RESTRICT"),
        nullable=False,
    )

    gpu_throughput_fp16: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    gpu_throughput_fp32: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    cpu_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)

    disk_read_mb_s: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    disk_write_mb_s: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    network_bandwidth_gbps: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)

    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    admin_verification_status: Mapped[str] = mapped_column(Text, nullable=False, server_default="pending")

    verified_by_admin_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.customer_id", ondelete="SET NULL"),
        nullable=True,
    )

    machine: Mapped["Machine"] = relationship("Machine", back_populates="benchmarks")

    verified_by_admin: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="verified_benchmarks",
        foreign_keys=[verified_by_admin_id],
    )

    __table_args__ = (
        CheckConstraint(
            "admin_verification_status IN ('pending', 'approved', 'rejected')",
            name="chk_benchmark_status",
        ),
        Index("idx_benchmarks_hardware_id", "hardware_id"),
        Index("idx_benchmarks_collected_at", "collected_at"),
        Index("idx_benchmarks_status", "admin_verification_status"),
    )