
from __future__ import annotations

from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Request

from app.auth import get_current_user
from app.users import User

from .schemas import PaymentRead, CheckoutRequest
from .public import PaymentsPublic, get_payments_public
from .service import PaymentsService, get_payments_service

router = APIRouter()


@router.get("/bookings/{booking_id}", response_model=list[PaymentRead])
def list_payments_for_booking(
    booking_id: UUID,
    payments_public: PaymentsPublic = Depends(get_payments_public),
    user: User = Depends(get_current_user),
):
    return payments_public.list_for_booking(booking_id)

# Stripe payment confirmation
# This endpoint is not applicable in a mock environment; in a production system,
# it would be used to retrieve a payment intent confirmation URL
@router.post("/checkout")
def create_checkout(
    checkout_data: CheckoutRequest,
    request: Request,
    payments_service: PaymentsService = Depends(get_payments_service),
    user=Depends(get_current_user),
):
    try:
        base_url = str(request.base_url) if request else "http://localhost:8000/"

        success_url = (
            f"{base_url}api/v1/payments/success"
            f"?session_id={{CHECKOUT_SESSION_ID}}"
            f"&booking_id={checkout_data.booking_id}"
        )
        cancel_url = f"{base_url}api/v1/payments/cancel?booking_id={checkout_data.booking_id}"

        result = payments_service.create_checkout_session(
            booking_id=checkout_data.booking_id,
            hardware_id=checkout_data.hardware_id,
            payer_id=user.customer_id,
            provider_id=None,
            amount=Decimal(str(checkout_data.amount)),
            currency=checkout_data.currency,
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=user.email,
        )

        return {"checkout_url": result.get("url"), "session_id": result.get("session_id")}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Verify Stripe Checkout Session
@router.get("/verify/{session_id}")
def verify_payment(
    session_id: str,
    payments_service: PaymentsService = Depends(get_payments_service),
):
    try:
        session = payments_service.verify_checkout_session(session_id)
        paid = session.get("payment_status") == "paid"
        return {"paid": paid, "session": session}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Marking invoice as paid, updating invoice's state in database
@router.patch("/mark-paid/{session_id}", response_model=PaymentRead)
def mark_paid(
    session_id: str,
    payments_service: PaymentsService = Depends(get_payments_service),
):
    try:
        return payments_service.mark_paid_by_invoice(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
