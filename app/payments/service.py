
from __future__ import annotations

from uuid import UUID
from decimal import Decimal
from typing import Dict, Any, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from .models import Payment
from .repository import PaymentsRepository
from .ports.payment_port import PaymentPort
from .ports.stripe_adapter import get_payment_adapter
from app.invoices import InvoicesService, get_invoices_service

_ALLOWED_STATUS = {"incomplete", "paid", "failed"}


class PaymentsService:
    def __init__(
        self,
        db: Session,
        repo: PaymentsRepository,
        port: PaymentPort,
        invoices_service: InvoicesService,
    ):
        self.db = db
        self.repo = repo
        self.port = port
        self.invoices = invoices_service

    def list_for_booking(self, booking_id: UUID):
        return self.repo.list_for_booking(self.db, booking_id)

    def get_payments_for_bookings(self, booking_ids: list[UUID]):
        return self.repo.list_for_bookings(self.db, booking_ids)

    # creates a Stripe Checkout Session and persists a Payment with status=incomplete
    # the Stripe session_id is stored in invoice_number
    def create_checkout_session(
        self,
        booking_id: UUID,
        hardware_id: UUID,
        payer_id: UUID,
        provider_id: Optional[UUID],
        amount: Decimal,
        currency: str,
        success_url: str,
        cancel_url: str,
        customer_email: str | None = None,
    ) -> Dict[str, Any]:
        result = self.port.create_checkout_session(
            booking_id=str(booking_id),
            user_id=str(payer_id),
            amount=amount,
            currency=currency,
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=customer_email,
        )

        session_id = result.get("session_id") or result.get("id") or result.get("sessionId")
        if not session_id:
            raise ValueError("Payment processor did not return session_id.")

        payment = Payment(
            booking_id=booking_id,
            hardware_id=hardware_id,
            payer_id=payer_id,
            provider_id=provider_id,
            amount_total=amount,
            currency=currency.upper(),
            payment_status="incomplete",
            invoice_number=str(session_id),
        )
        self.repo.create(self.db, payment)

        return result

    # development purposes helper: records payment directly to the database, bypassing Stripe
    def create_dummy_for_booking(
        self,
        booking_id: UUID,
        hardware_id: UUID,
        payer_id: UUID,
        provider_id: Optional[UUID],
        amount_total: Decimal,
        currency: str = "EUR",
        status: str = "paid",
        invoice_number: str | None = None,
    ) -> Payment:
        """
        DEV/demo helper: direktno upisuje Payment u bazu bez Stripe-a.
        """
        if status not in _ALLOWED_STATUS:
            raise ValueError(f"Invalid payment status: {status}")

        payment = Payment(
            booking_id=booking_id,
            hardware_id=hardware_id,
            payer_id=payer_id,
            provider_id=provider_id,
            amount_total=amount_total,
            currency=currency.upper(),
            payment_status=status,
            invoice_number=invoice_number,
        )
        return self.repo.create(self.db, payment)

    def verify_checkout_session(self, session_id: str) -> Dict[str, Any]:
        return self.port.retrieve_checkout_session(session_id=session_id)

    def mark_paid_by_invoice(self, invoice_number: str) -> Payment:
        try:
            payment = self.repo.get_by_invoice_number(self.db, invoice_number)
            if not payment:
                raise ValueError("Payment not found for this invoice_number.")

            payment.payment_status = "paid"
            payment = self.repo.update(self.db, payment)

            self.invoices.mark_paid_by_number(invoice_number)

            return payment
        except Exception:
            self.db.rollback()
            raise

    def mark_failed_by_invoice(self, invoice_number: str) -> Payment:
        payment = self.repo.get_by_invoice_number(self.db, invoice_number)
        if not payment:
            raise ValueError("Payment not found for this invoice_number.")
        payment.payment_status = "failed"
        return self.repo.update(self.db, payment)


def get_payments_service(
    db: Session = Depends(get_db),
    port: PaymentPort = Depends(get_payment_adapter),
    invoices_service: InvoicesService = Depends(get_invoices_service),
) -> PaymentsService:
    return PaymentsService(
        db=db,
        repo=PaymentsRepository(),
        port=port,
        invoices_service=invoices_service,
    )