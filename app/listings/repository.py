
from __future__ import annotations

from uuid import UUID
from sqlalchemy.orm import Session, joinedload

from .models import Listing

class ListingsRepository:
    def get_listings(self, db: Session) -> list[Listing]:
        return (
            db.query(Listing)
            .options(joinedload(Listing.machine))
            .order_by(Listing.updated_at.desc().nullslast(), Listing.created_at.desc())
            .all()
        )

    def create_listing(self, db: Session, listing: Listing) -> Listing:
        db.add(listing)
        db.commit()
        db.refresh(listing)
        return listing

    def get_listing_by_id(self, db: Session, listing_id: UUID) -> Listing | None:
        return db.get(Listing, listing_id)