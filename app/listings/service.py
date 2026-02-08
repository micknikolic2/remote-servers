
from __future__ import annotations

from uuid import UUID
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from .repository import ListingsRepository
from .models import Listing
from .schemas import ListingCreate


_ALLOWED_STATUS = {"active", "paused", "archived"}


class ListingsService:
    def __init__(
        self,
        db: Session,
        listings_repo: ListingsRepository,
    ):
        self.db = db
        self.listings_repo = listings_repo


    def list_listings(self) -> list[Listing]:
        return self.listings_repo.get_listings(self.db)

    def get_listing_by_id(self, listing_id: UUID) -> Listing:
        listing = self.listings_repo.get_listing_by_id(self.db, listing_id)
        if not listing:
            raise ValueError("Listing not found.")
        return listing


    def create_listing(self, customer_id: UUID, payload: ListingCreate) -> Listing:
        machine = self.machines_repo.get_machine(self.db, payload.hardware_id)
        if not machine:
            raise ValueError("Machine not found.")
        if machine.customer_id != customer_id:
            raise ValueError("Not allowed: you do not own this machine.")

        self._validate_payload(payload)

        listing = Listing(
            hardware_id=payload.hardware_id,
            price_hour=payload.price_hour,
            price_day=payload.price_day,
            price_week=payload.price_week,
            currency=payload.currency.upper(),
            status=payload.status,
            updated_at=datetime.now(timezone.utc),
        )
        return self.listings_repo.create_listing(self.db, listing)


    # domain-level validation beyond schema constraints
    def _validate_payload(self, payload: ListingCreate) -> None:
        if not payload.currency or len(payload.currency.strip()) != 3:
            raise ValueError("currency must be a 3-letter code (e.g. 'EUR').")

        if payload.status not in _ALLOWED_STATUS:
            raise ValueError("status must be one of: active, paused, archived.")

        if payload.price_hour is None and payload.price_day is None and payload.price_week is None:
            raise ValueError("At least one of price_hour, price_day, price_week must be provided.")

        for name, value in (
            ("price_hour", payload.price_hour),
            ("price_day", payload.price_day),
            ("price_week", payload.price_week),
        ):
            if value is None:
                continue
            if Decimal(value) < 0:
                raise ValueError(f"{name} must be >= 0.")

# Dependency provider for ListingsService
def get_listings_service(db: Session = Depends(get_db)) -> ListingsService:
    return ListingsService(
        db=db,
        listings_repo=ListingsRepository(),
    )
