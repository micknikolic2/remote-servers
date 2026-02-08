
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from .service import MetricsService, get_metrics_service
from .schemas import MetricSampleCreate, MetricsQueryParams, MetricSampleRead, MetricSampleListItem

from app.auth import get_current_user
from app.users import User

router = APIRouter()


@router.post(
    "/machines/{hardware_id}/ingest",
    response_model=MetricSampleRead,
    summary="Submit a metric sample for a machine",
)
def ingest_metric_sample(
    hardware_id: UUID,
    payload: MetricSampleCreate,
    service: MetricsService = Depends(get_metrics_service),
    user: User = Depends(get_current_user),
):
    try:
        return service.ingest_metrics(
            hardware_id=hardware_id,
            payload=payload,
            customer_id=user.customer_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get(
    "/machines/{hardware_id}",
    response_model=list[MetricSampleListItem],
    summary="List metrics for a machine",
)
def list_metrics_for_machine(
    hardware_id: UUID,
    query: MetricsQueryParams = Depends(),
    user: User = Depends(get_current_user),
    service: MetricsService = Depends(get_metrics_service),
):
    try:
        return service.list_machine_metrics(hardware_id, query)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/machines/{hardware_id}/latest",
    response_model=MetricSampleRead | None,
    summary="Get latest metric sample for a machine",
)
def get_latest_metrics(
    hardware_id: UUID,
    user: User = Depends(get_current_user),
    service: MetricsService = Depends(get_metrics_service),
):
    try:
        return service.get_latest_metrics(hardware_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
