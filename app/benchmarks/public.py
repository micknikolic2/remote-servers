from typing import List
from uuid import UUID
from typing_extensions import Protocol

from fastapi import Depends

from .service import BenchmarkService, get_benchmark_service
from .models import Benchmark


# Public read-only interface for benchmark access
# Acts as an abstraction over the underlying service layer
class BenchmarksPublic(Protocol):
    def get_benchmarks_for_machine(self, hardware_id: UUID) -> List[Benchmark]:
        pass

# Default BenchmarkPublic implementation, delegates all operations to BenchmarkService
class BenchmarksPublicImpl(BenchmarksPublic):
    def __init__(self, service: BenchmarkService):
        self.service = service

    def get_benchmarks_for_machine(self, hardware_id: UUID) -> List[Benchmark]:
        return self.service.list_machine_benchmarks(hardware_id)

# Dependency provider wiring the public interface to its implementation
def get_benchmarks_public(
    service: BenchmarkService = Depends(get_benchmark_service),
) -> BenchmarksPublic:
    return BenchmarksPublicImpl(service)
