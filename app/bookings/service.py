
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from .repository import BookingsRepository
from .models import Booking
from .schemas import BookingRequest, BookingAdminCreate

from app.listings import ListingsPublic, get_listings_public

from app.invoices import InvoicesService, get_invoices_service
from app.payments import PaymentsService, get_payments_service


class BookingsService:
    def __init__(
        self,
        db: Session,
        repo: BookingsRepository,
        listings_public: ListingsPublic,
        invoices_service: InvoicesService,
        payments_service: PaymentsService,
    ):
        self.db = db
        self.repo = repo
        self.listings_public = listings_public
        self.invoices = invoices_service
        self.payments = payments_service

    # Normalizes timestamps to UTC and validates the requested interval
    # Prevents timezone bugs and ensures end > start
    def _normalize_times(self, start_ts: datetime, end_ts: datetime):
        if start_ts.tzinfo is None or end_ts.tzinfo is None:
            raise ValueError("start_timestamp and end_timestamp must be timezone-aware")
        start_utc = start_ts.astimezone(timezone.utc)
        end_utc = end_ts.astimezone(timezone.utc)
        if end_utc <= start_utc:
            raise ValueError("end_timestamp must be after start_timestamp")
        return start_utc, end_utc

     # Computes booking amount based on duration and listing pricing
    def _calculate_amount(self, start_utc: datetime, end_utc: datetime, listing) -> Decimal:
        seconds = Decimal(str((end_utc - start_utc).total_seconds()))
        hours = seconds / Decimal("3600")

        price_hour = getattr(listing, "price_hour", None)
        if price_hour is None:
            return Decimal("0.00")

        hourly = price_hour if isinstance(price_hour, Decimal) else Decimal(str(price_hour))
        amount = hours * hourly
        return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Read-only lookup
    def get_booking_readonly(self, booking_id: UUID) -> Booking:
        booking = self.repo.get_booking_by_id(self.db, booking_id)
        if not booking:
            raise ValueError("Booking not found")
        return booking

    def list_bookings_for_user(self, buyer_id: UUID):
        return self.repo.list_bookings_for_user(self.db, buyer_id)

    # Admin visibility: list all bookings in the system
    def list_all_bookings(self):
        return self.repo.list_bookings(self.db)

    # Booking creation
    def request_booking(self, buyer_id: UUID, payload: BookingRequest) -> Booking:
        # 1) validate/normalize time range
        start_utc, end_utc = self._normalize_times(payload.start_timestamp, payload.end_timestamp)

        # 2) load listing + machine
        listing = self.listings_public.get_listing_by_id(payload.listing_id)
        if not listing:
            raise ValueError("Listing not found")

        machine = listing.machine
        if not machine:
            raise ValueError("Listing has no machine attached")

        # 3) persist booking
        booking = Booking(
            listing_id=payload.listing_id,
            hardware_id=machine.hardware_id,
            buyer_id=buyer_id,
            start_timestamp=start_utc,
            end_timestamp=end_utc,
            #pending until payment flow completed
            booking_status="pending", 
        )
        created = self.repo.create_booking(self.db, booking)

        # 4) create invoice
        amount = self._calculate_amount(start_utc, end_utc, listing)
        currency = getattr(listing, "currency", "EUR") or "EUR"

        invoice = self.invoices.create_invoice_for_booking(
            booking=created,
            payer_id=buyer_id,
            provider_id=machine.customer_id,
            amount_total=amount,
            currency=currency,
        )

        # 5) create initial payment record (currently dummy/incomplete)
        self.payments.create_dummy_for_booking(
            booking_id=created.booking_id,
            hardware_id=created.hardware_id,
            payer_id=buyer_id,
            provider_id=machine.customer_id,
            amount_total=amount,
            currency=currency,
            status="incomplete",
            invoice_number=invoice.invoice_number,
        )

        return created

    # Admin helper: creates a booking on behalf of a user by reusing the same flow
    def admin_create_booking(self, payload: BookingAdminCreate) -> Booking:
        req = BookingRequest(
            listing_id=payload.listing_id,
            start_timestamp=payload.start_timestamp,
            end_timestamp=payload.end_timestamp,
        )
        return self.request_booking(payload.buyer_id, req)

# Dependency provider wiring the service and its collaborators
def get_bookings_service(
    db: Session = Depends(get_db),
    listings_public: ListingsPublic = Depends(get_listings_public),
    invoices_service: InvoicesService = Depends(get_invoices_service),
    payments_service: PaymentsService = Depends(get_payments_service),
) -> BookingsService:
    return BookingsService(
        db=db,
        repo=BookingsRepository(),
        listings_public=listings_public,
        invoices_service=invoices_service,
        payments_service=payments_service,
    )
