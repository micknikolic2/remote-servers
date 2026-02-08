
from __future__ import annotations

from typing import Protocol, List
from uuid import UUID

from fastapi import Depends

from .service import PaymentsService, get_payments_service
from .models import Payment

# Public facade for payment-related read operations
class PaymentsPublic(Protocol):
    def list_for_booking(self, booking_id: UUID) -> List[Payment]:
        pass

    def get_payments_for_bookings(self, booking_ids: list[UUID]) -> List[Payment]:
        pass

# Default implementation of PaymentsPublic
class PaymentsPublicImpl(PaymentsPublic):
    def __init__(self, service: PaymentsService):
        self.service = service

    def list_for_booking(self, booking_id: UUID) -> List[Payment]:
        return self.service.list_for_booking(booking_id)

    def get_payments_for_bookings(self, booking_ids: list[UUID]) -> List[Payment]:
        return self.service.get_payments_for_bookings(booking_ids)

# Dependency provider wiring public facade with service implementation
def get_payments_public(service: PaymentsService = Depends(get_payments_service)) -> PaymentsPublic:
    return PaymentsPublicImpl(service)
