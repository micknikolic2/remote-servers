
from __future__ import annotations

from typing import Protocol
from uuid import UUID

from fastapi import Depends
from .service import MachinesService, get_machines_service

# Public facade for machine-related read checks
class MachinesPublic(Protocol):
    def customer_owns_machine(self, customer_id: UUID, machine_id: UUID) -> bool:
        pass

    def get_machine(self, machine_id: UUID):
        pass

    def list_machines_for_customer(self, customer_id: UUID):
        pass

# Default implementation of MachinesPublic
class MachinesPublicImpl:
    def __init__(self, service: MachinesService):
        self.service = service

    def customer_owns_machine(self, customer_id: UUID, machine_id: UUID) -> bool:
        try:
            machine = self.service.get_machine(machine_id)
        except ValueError:
            return False
        return machine.customer_id == customer_id

    def get_machine(self, machine_id: UUID):
        return self.service.get_machine(machine_id)

    def list_machines_for_customer(self, customer_id: UUID):
        return self.service.list_machines_for_customer(customer_id)

# Dependency provider wiring the public facade to the service layer
def get_machines_public(service: MachinesService = Depends(get_machines_service)) -> MachinesPublic:
    return MachinesPublicImpl(service)
