
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException

from app.auth import get_current_user
from app.users import User

from .schemas import MachineCreate, MachineRead
from .service import MachinesService, get_machines_service

router = APIRouter()


@router.get("/{machine_id:uuid}", response_model=MachineRead)
def get_machine(
    machine_id: UUID,
    user: User = Depends(get_current_user),
    service: MachinesService = Depends(get_machines_service),
):
    try:
        machine = service.get_machine(machine_id)
    except ValueError:
        raise HTTPException(404, "Machine not found")

    if machine.customer_id != user.customer_id:
        raise HTTPException(403, "Not allowed")

    return machine


@router.get("/", response_model=list[MachineRead])
def list_machines(
    user: User = Depends(get_current_user),
    service: MachinesService = Depends(get_machines_service),
):
    return service.list_machines_for_customer(user.customer_id)


@router.delete("/{machine_id:uuid}", status_code=204)
def delete_machine(
    machine_id: UUID,
    user: User = Depends(get_current_user),
    service: MachinesService = Depends(get_machines_service),
):
    try:
        service.delete_machine(machine_id, customer_id=user.customer_id)
    except ValueError as e:
        msg = str(e)
        if "does not exist" in msg:
            raise HTTPException(404, "Machine not found")
        if "own" in msg:
            raise HTTPException(403, "Not allowed")
        raise


@router.post("/", response_model=MachineRead, status_code=201)
def create_machine(
    machine: MachineCreate,
    user: User = Depends(get_current_user),
    service: MachinesService = Depends(get_machines_service),
):
    machine.customer_id = user.customer_id
    try:
        return service.create_machine(payload=machine)
    except ValueError as e:
        raise HTTPException(400, str(e))
