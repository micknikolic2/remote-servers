from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.users import User

from .service import BenchmarkService, get_benchmark_service
from .schemas import BenchmarkCreate, BenchmarkRead

router = APIRouter()

@router.post(
    "/machines/{hardware_id}",
    response_model=BenchmarkRead,
    status_code=status.HTTP_201_CREATED,
)
def create_machine_benchmark(
    hardware_id: UUID,
    payload: BenchmarkCreate,
    user: User = Depends(get_current_user),
    service: BenchmarkService = Depends(get_benchmark_service),
):
    payload = payload.model_copy(update={"hardware_id": hardware_id})

    try:
        obj = service.create_benchmark(
            provider_id=user.customer_id,
            payload=payload,
        )
        return obj
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/machines/{hardware_id}",
    response_model=list[BenchmarkRead],
)
def get_machine_benchmarks(
    hardware_id: UUID,
    service: BenchmarkService = Depends(get_benchmark_service),
    user: User = Depends(get_current_user),
):
    try:
        return service.list_machine_benchmarks(hardware_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))