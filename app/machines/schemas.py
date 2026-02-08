
from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional, Dict, Any

# API contract models (DTOs) for machine endpoints
# These schemas define external endpoint contract
class MachineCreate(BaseModel):
    customer_id: Optional[UUID] = None

    gpu_model: Optional[str] = None
    cpu_model: Optional[str] = None

    ram_gb: int = Field(..., gt=0)

    disk_type: Optional[str] = None
    disk_size_gb: Optional[int] = Field(default=None, gt=0)

    network_bandwidth: Optional[str] = None
    os: Optional[str] = None

    provider_agent_status: str = Field(default="offline", pattern="^(online|offline)$")
    health_indicators: Optional[Dict[str, Any]] = None


class MachineRead(BaseModel):
    hardware_id: UUID
    customer_id: UUID

    gpu_model: Optional[str] = None
    cpu_model: Optional[str] = None
    ram_gb: int

    disk_type: Optional[str] = None
    disk_size_gb: Optional[int] = None

    network_bandwidth: Optional[str] = None
    os: Optional[str] = None

    provider_agent_status: str
    health_indicators: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)
