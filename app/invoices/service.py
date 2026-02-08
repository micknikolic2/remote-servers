
from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from .repository import InvoicesRepository
from .models import Invoice
from .schemas import InvoiceCreate


class InvoicesService:
    def __init__(self, db: Session, repo: InvoicesRepository):
        self.db = db
        self.repo = repo

    def create_invoice(self, payload: InvoiceCreate) -> Invoice:
        # prevent duplicates per booking
        existing = self.repo.get_by_booking(self.db, payload.booking_id)
        if existing:
            return existing

        invoice_number = self._generate_invoice_number()

        inv = Invoice(
            booking_id=payload.booking_id,
            payer_id=payload.payer_id,
            provider_id=payload.provider_id,
            amount_total=payload.amount_total,
            currency=payload.currency.upper(),
            status="issued",
            issued_at=datetime.now(timezone.utc),
            invoice_number=invoice_number,
            notes=payload.notes,
        )
        return self.repo.create(self.db, inv)

    def mark_paid(self, invoice_id: UUID) -> Invoice:
        inv = self.repo.get(self.db, invoice_id)
        if not inv:
            raise ValueError("Invoice not found.")
        inv.status = "paid"
        inv.paid_at = datetime.now(timezone.utc)
        return self.repo.update(self.db, inv)
    
    def mark_paid_by_number(self, invoice_number: str) -> Invoice:
        inv = self.repo.get_by_invoice_number(self.db, invoice_number)
        if not inv:
            raise ValueError("Invoice not found.")
        inv.status = "paid"
        inv.paid_at = datetime.now(timezone.utc)
        return self.repo.update(self.db, inv)


    def _generate_invoice_number(self) -> str:
        now = datetime.now(timezone.utc)
        suffix = int(now.timestamp() * 1000) % 1_000_000_000
        return f"INV-{now.year}-{suffix:09d}"
    
    def create_invoice_for_booking(self, booking, payer_id, provider_id, amount_total, currency="EUR"):
        existing = self.repo.get_by_booking(self.db, booking.booking_id)
        if existing:
            return existing

        inv = Invoice(
            booking_id=booking.booking_id,
            payer_id=payer_id,
            provider_id=provider_id,
            amount_total=amount_total,
            currency=currency.upper(),
            status="issued",
            issued_at=datetime.now(timezone.utc),
            invoice_number=self._generate_invoice_number(),
        )
        return self.repo.create(self.db, inv)

# Dependency provider wiring the service and its collaborators
def get_invoices_service(db: Session = Depends(get_db)) -> InvoicesService:
    return InvoicesService(db=db, repo=InvoicesRepository())
