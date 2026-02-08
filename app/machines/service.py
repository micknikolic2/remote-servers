
from __future__ import annotations

from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from .repository import MachinesRepository
from .schemas import MachineCreate
from .models import Machine

# Service layer for machine-related business operations
class MachinesService:
    def __init__(self, db: Session, machine_repo: MachinesRepository):
        self.db = db
        self.machine_repo = machine_repo

    def get_machine(self, machine_id: UUID) -> Machine:
        machine = self.machine_repo.get_machine(self.db, machine_id)
        if not machine:
            raise ValueError("Machine does not exist.")
        return machine

    def list_machines_for_customer(self, customer_id: UUID) -> list[Machine]:
        return self.machine_repo.list_machines_for_customer(self.db, customer_id)

    def create_machine(self, payload: MachineCreate) -> Machine:
        if payload.customer_id is None:
            raise ValueError("customer_id is required.")
        return self.machine_repo.create_machine(self.db, payload)

    # ownership check: only the owner can delete the machine
    def delete_machine(self, machine_id: UUID, customer_id: UUID):
        machine = self.machine_repo.get_machine(self.db, machine_id)
        if not machine:
            raise ValueError("Machine does not exist.")
        if machine.customer_id != customer_id:
            raise ValueError("You do not own this machine.")
        self.machine_repo.delete_machine(self.db, machine)

# Dependency provider for MachinesService
def get_machines_service(db: Session = Depends(get_db)) -> MachinesService:
    return MachinesService(db=db, machine_repo=MachinesRepository())
