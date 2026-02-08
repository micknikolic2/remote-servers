
from __future__ import annotations

from uuid import UUID
from typing import Optional, List

from sqlalchemy.orm import Session

from .models import Payment


class PaymentsRepository:
    def create(self, db: Session, payment: Payment) -> Payment:
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    def update(self, db: Session, payment: Payment) -> Payment:
        db.commit()
        db.refresh(payment)
        return payment

    def get(self, db: Session, payment_id: UUID) -> Optional[Payment]:
        return db.get(Payment, payment_id)

    def list_for_booking(self, db: Session, booking_id: UUID) -> List[Payment]:
        return (
            db.query(Payment)
            .filter(Payment.booking_id == booking_id)
            .order_by(Payment.timestamp.asc())
            .all()
        )

    def list_for_bookings(self, db: Session, booking_ids: list[UUID]) -> list[Payment]:
        if not booking_ids:
            return []
        return (
            db.query(Payment)
            .filter(Payment.booking_id.in_(booking_ids))
            .order_by(Payment.timestamp.asc())
            .all()
        )

    def get_by_invoice_number(self, db: Session, invoice_number: str) -> Optional[Payment]:
        return (
            db.query(Payment)
            .filter(Payment.invoice_number == invoice_number)
            .first()
        )
