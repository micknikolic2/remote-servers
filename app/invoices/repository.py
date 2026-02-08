
from uuid import UUID
from sqlalchemy.orm import Session
from .models import Invoice


class InvoicesRepository:
    def create(self, db: Session, invoice: Invoice) -> Invoice:
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice

    def get_by_booking(self, db: Session, booking_id: UUID) -> Invoice | None:
        return db.query(Invoice).filter(Invoice.booking_id == booking_id).first()

    def get(self, db: Session, invoice_id: UUID) -> Invoice | None:
        return db.get(Invoice, invoice_id)

    def update(self, db: Session, invoice: Invoice) -> Invoice:
        db.commit()
        db.refresh(invoice)
        return invoice

    def get_by_invoice_number(self, db: Session, invoice_number: str) -> Invoice | None:
        return db.query(Invoice).filter(Invoice.invoice_number == invoice_number).first()

