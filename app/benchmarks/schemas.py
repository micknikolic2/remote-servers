from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# API schema models for benchmark endpoints
# These models define the external API contract
class BenchmarkCreate(BaseModel):
    """
    Request model: Provider submits benchmark sample for a machine.
    Admin verification is separate.
    """
    hardware_id: UUID

    gpu_throughput_fp16: Optional[Decimal] = Field(None)
    gpu_throughput_fp32: Optional[Decimal] = Field(None)
    cpu_score: Optional[Decimal] = Field(None)

    disk_read_mb_s: Optional[Decimal] = Field(None)
    disk_write_mb_s: Optional[Decimal] = Field(None)
    network_bandwidth_gbps: Optional[Decimal] = Field(None)

    collected_at: datetime


class BenchmarkRead(BaseModel):
    """Response model returned by benchmark endpoints."""
    benchmark_id: UUID
    hardware_id: UUID

    gpu_throughput_fp16: Optional[Decimal]
    gpu_throughput_fp32: Optional[Decimal]
    cpu_score: Optional[Decimal]
    disk_read_mb_s: Optional[Decimal]
    disk_write_mb_s: Optional[Decimal]
    network_bandwidth_gbps: Optional[Decimal]

    collected_at: datetime
    admin_verification_status: str
    verified_by_admin_id: Optional[UUID]

    model_config = ConfigDict(from_attributes=True)
