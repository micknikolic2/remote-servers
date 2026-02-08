
from fastapi import Depends
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from .repository import MetricsRepository
from .schemas import (
    MetricSampleCreate,
    MetricSampleRead,
    MetricSampleListItem,
    MetricsQueryParams,
)

from app.machines import MachinesPublic, get_machines_public
from app.database import get_db


class MetricsService:
    def __init__(
        self,
        db: Session,
        repo: MetricsRepository,
        machines_public: MachinesPublic,
    ):
        self.db = db
        self.repo = repo
        self.machines_public = machines_public

    # ingests a validated metric sample for a machine
    def ingest_metrics(
        self,
        hardware_id: UUID,
        payload: MetricSampleCreate,
        customer_id: UUID,
    ) -> MetricSampleRead:
        machine = self.machines_public.get_machine(hardware_id)
        if not machine:
            raise ValueError("Machine does not exist.")

        # only machine owner can ingest metrics
        if not self.machines_public.customer_owns_machine(
            customer_id=customer_id,
            machine_id=hardware_id,
        ):
            raise PermissionError("User does not own machine.")

        # if client doesn't provide a timestamp, record ingestion time in UTC
        recorded_at = payload.recorded_at or datetime.now(timezone.utc)

        sample = self.repo.create_sample(
            self.db,
            hardware_id=hardware_id,
            recorded_at=recorded_at,
            gpu_util=payload.gpu_util,
            cpu_util=payload.cpu_util,
            mem_used_gb=payload.mem_used_gb,
            net_rx_mb=payload.net_rx_mb,
            net_tx_mb=payload.net_tx_mb,
        )

        return MetricSampleRead.model_validate(sample)

    # adapter for raw payloads (best-effort mapping to MetricSampleCreate)
    def ingest_raw_metrics(self, hardware_id: UUID, raw: dict, customer_id: UUID):
        payload = MetricSampleCreate(
            recorded_at=raw.get("collected_at"),
            gpu_util=raw.get("gpu_util"),
            cpu_util=raw.get("cpu_util"),
            mem_used_gb=raw.get("mem_gb"),
            net_rx_mb=raw.get("net_rx_mb"),
            net_tx_mb=raw.get("net_tx_mb"),
        )
        return self.ingest_metrics(hardware_id=hardware_id, payload=payload, customer_id=customer_id)

    # lists metric samples for a machine within a time window
    def list_machine_metrics(
        self,
        hardware_id: UUID,
        query: MetricsQueryParams,
    ) -> list[MetricSampleListItem]:
        machine = self.machines_public.get_machine(hardware_id)
        if not machine:
            raise ValueError("Machine does not exist.")

        samples = self.repo.list_samples(
            self.db,
            hardware_id=hardware_id,
            start=query.start,
            end=query.end,
            limit=query.limit,
        )

        return [MetricSampleListItem.model_validate(s) for s in samples]

    # returns the most recent metric sample for a machine (or None if no samples exist)
    def get_latest_metrics(
        self,
        hardware_id: UUID,
    ) -> Optional[MetricSampleRead]:
        machine = self.machines_public.get_machine(hardware_id)
        if not machine:
            raise ValueError("Machine does not exist.")

        sample = self.repo.get_latest_sample(self.db, hardware_id)
        if not sample:
            return None

        return MetricSampleRead.model_validate(sample)

# Dependency provider for MetricsService
def get_metrics_service(
    db: Session = Depends(get_db),
    machines_public: MachinesPublic = Depends(get_machines_public),
) -> MetricsService:
    return MetricsService(db=db, repo=MetricsRepository(), machines_public=machines_public)
