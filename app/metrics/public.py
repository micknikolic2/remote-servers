from typing import Protocol, Optional
from uuid import UUID

from fastapi import Depends

from .service import MetricsService, get_metrics_service
from .schemas import MetricSampleListItem, MetricSampleRead, MetricsQueryParams

# Protocol defining the public interface for machines queries
class MetricsPublic(Protocol):
    def get_latest_metrics(self, hardware_id: UUID) -> Optional[MetricSampleRead]:
        pass

    def list_metrics_for_machine(
        self,
        hardware_id: UUID,
        query: MetricsQueryParams,
    ) -> list[MetricSampleListItem]:
        pass

    def ingest_raw_metrics(self, hardware_id: UUID, raw: dict, customer_id: UUID):
        pass

# Concrete implementation of MetricsPublic using the MetricsService
class MetricsPublicImpl:
    def __init__(self, service: MetricsService):
        self.service = service

    def get_latest_metrics(self, hardware_id: UUID) -> Optional[MetricSampleRead]:
        return self.service.get_latest_metrics(hardware_id)

    def list_metrics_for_machine(
        self,
        hardware_id: UUID,
        query: MetricsQueryParams,
    ) -> list[MetricSampleListItem]:
        return self.service.list_machine_metrics(hardware_id, query)
    
    def ingest_raw_metrics(self, hardware_id: UUID, raw: dict, customer_id: UUID):
        return self.service.ingest_raw_metrics(hardware_id, raw, customer_id)

# Dependency injection provider for MetricsService interface
def get_metrics_public(
    service: MetricsService = Depends(get_metrics_service),
) -> MetricsPublic:
    return MetricsPublicImpl(service)