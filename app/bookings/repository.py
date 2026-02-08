
from __future__ import annotations

from uuid import UUID
from sqlalchemy.orm import Session

from .models import Booking

class BookingsRepository:
    def create_booking(self, db: Session, booking: Booking) -> Booking:
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    def update_booking(self, db: Session, booking: Booking) -> Booking:
        db.commit()
        db.refresh(booking)
        return booking

    def get_booking_by_id(self, db: Session, booking_id: UUID) -> Booking | None:
        return db.get(Booking, booking_id)

    def list_bookings(self, db: Session) -> list[Booking]:
        return (
            db.query(Booking)
            .order_by(Booking.created_at.desc())
            .all()
        )

    def list_bookings_for_user(self, db: Session, buyer_id: UUID) -> list[Booking]:
        return (
            db.query(Booking)
            .filter(Booking.buyer_id == buyer_id)
            .order_by(Booking.start_timestamp.desc())
            .all()
        )
