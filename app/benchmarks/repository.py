from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from .models import Benchmark


class BenchmarksRepository:
    def create(self, db: Session, obj: Benchmark) -> Benchmark:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(self, db: Session, benchmark_id: UUID) -> Optional[Benchmark]:
        return db.get(Benchmark, benchmark_id)

    def list_for_machine(self, db: Session, hardware_id: UUID) -> List[Benchmark]:
        stmt = (
            select(Benchmark)
            .where(Benchmark.hardware_id == hardware_id)
            .order_by(desc(Benchmark.collected_at))
        )
        return list(db.scalars(stmt).all())

    def list_latest_approved_for_machine(
        self, db: Session, hardware_id: UUID, limit: int = 1
    ) -> List[Benchmark]:
        stmt = (
            select(Benchmark)
            .where(
                Benchmark.hardware_id == hardware_id,
                Benchmark.admin_verification_status == "approved",
            )
            .order_by(desc(Benchmark.collected_at))
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    def update(self, db: Session, obj: Benchmark) -> Benchmark:
        db.commit()
        db.refresh(obj)
        return obj
