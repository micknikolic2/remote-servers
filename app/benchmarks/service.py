from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.machines import MachinesPublic, get_machines_public

from .models import Benchmark
from .repository import BenchmarksRepository
from .schemas import BenchmarkCreate

# Service layer for benchmark-related business logic
class BenchmarkService:
    def __init__(
        self,
        db: Session,
        repo: BenchmarksRepository,
        machines_public: MachinesPublic,
    ):
        self.db = db
        self.repo = repo
        self.machines_public = machines_public

    # Creates a benchmark submission for a machines
    def create_benchmark(
        self,
        provider_id: UUID,
        payload: BenchmarkCreate,
    ) -> Benchmark:
        # Authorization check: provider must own the target machine
        if not self.machines_public.customer_owns_machine(
            customer_id=provider_id,
            machine_id=payload.hardware_id,
        ):
            raise PermissionError("User does not own this machine")

        # Map request payload to domain model (no direct DB exposure)
        obj = Benchmark(
            hardware_id=payload.hardware_id,
            gpu_throughput_fp16=payload.gpu_throughput_fp16,
            gpu_throughput_fp32=payload.gpu_throughput_fp32,
            cpu_score=payload.cpu_score,
            disk_read_mb_s=payload.disk_read_mb_s,
            disk_write_mb_s=payload.disk_write_mb_s,
            network_bandwidth_gbps=payload.network_bandwidth_gbps,
            collected_at=payload.collected_at,
        )
        return self.repo.create(self.db, obj)

    # Returns all benchmarks for a given machines
    def list_machine_benchmarks(self, hardware_id: UUID) -> List[Benchmark]:
        machine = self.machines_public.get_machine(hardware_id)
        if not machine:
            raise ValueError("Machine does not exist.")
        return self.repo.list_for_machine(self.db, hardware_id)


# Dependency provider wiring the service with its collaborators
def get_benchmark_service(
    db: Session = Depends(get_db),
    machines_public: MachinesPublic = Depends(get_machines_public),
) -> BenchmarkService:
    return BenchmarkService(
        db=db,
        repo=BenchmarksRepository(),
        machines_public=machines_public,
    )
