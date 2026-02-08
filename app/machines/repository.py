
from __future__ import annotations

from uuid import UUID
from sqlalchemy.orm import Session

from .models import Machine
from .schemas import MachineCreate


class MachinesRepository:
    def create_machine(self, db: Session, machine_data: MachineCreate) -> Machine:
        db_machine = Machine(
            customer_id=machine_data.customer_id,
            gpu_model=machine_data.gpu_model,
            cpu_model=machine_data.cpu_model,
            ram_gb=machine_data.ram_gb,
            disk_type=machine_data.disk_type,
            disk_size_gb=machine_data.disk_size_gb,
            network_bandwidth=machine_data.network_bandwidth,
            os=machine_data.os,
            provider_agent_status=machine_data.provider_agent_status,
            health_indicators=machine_data.health_indicators,
        )
        db.add(db_machine)
        db.commit()
        db.refresh(db_machine)
        return db_machine

    def get_machine(self, db: Session, machine_id: UUID) -> Machine | None:
        return (
            db.query(Machine)
            .filter(Machine.hardware_id == machine_id)
            .first()
        )

    def list_machines_for_customer(self, db: Session, customer_id: UUID) -> list[Machine]:
        return (
            db.query(Machine)
            .filter(Machine.customer_id == customer_id)
            .all()
        )

    def customer_owns_machine(self, db: Session, customer_id: UUID, machine_id: UUID) -> bool:
        return (
            db.query(Machine)
            .filter(
                Machine.hardware_id == machine_id,
                Machine.customer_id == customer_id,
            )
            .count()
            > 0
        )

    def delete_machine(self, db: Session, machine: Machine) -> None:
        db.delete(machine)
        db.commit()
