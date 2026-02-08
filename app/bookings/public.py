
from typing import Protocol
from uuid import UUID

from fastapi import Depends

from .service import BookingsService, get_bookings_service

# Public read-only interface for booking access
class BookingsPublic(Protocol):

    def get_booking(self, booking_id: UUID):
        pass

    def is_pending(self, booking) -> bool:
        pass

    def is_active(self, booking) -> bool:
        pass

    def is_completed(self, booking) -> bool:
        pass

    def is_canceled(self, booking) -> bool:
        pass

    def is_disputed(self, booking) -> bool:
        pass

# Default BenchmarkPublic implementation, basig getters
class BookingsPublicImpl:
    def __init__(self, service: BookingsService):
        self.service = service

    def get_booking(self, booking_id: UUID):
        return self.service.get_booking_readonly(booking_id)

    def is_pending(self, booking) -> bool:
        return booking.booking_status == "pending"

    def is_active(self, booking) -> bool:
        return booking.booking_status == "active"

    def is_completed(self, booking) -> bool:
        return booking.booking_status == "completed"

    def is_canceled(self, booking) -> bool:
        return booking.booking_status == "canceled"

    def is_disputed(self, booking) -> bool:
        return booking.booking_status == "disputed"

# Dependency provider wiring the public interface to its implementation
def get_bookings_public(
    service: BookingsService = Depends(get_bookings_service),
) -> BookingsPublic:
    return BookingsPublicImpl(service)
