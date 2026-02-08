"""
Endpoints for listing servers.
Authenticated users can create listings for machines they own.
Everyone can browse listings.
"""

from __future__ import annotations

from fastapi import Depends, APIRouter, HTTPException
from uuid import UUID

from app.auth import get_current_user
from app.users import User

from .schemas import ListingCreate, ListingRead
from .service import ListingsService, get_listings_service

router = APIRouter()

@router.post("/", response_model=ListingRead, status_code=201)
def create_listing(
    listing: ListingCreate,
    user: User = Depends(get_current_user),
    service: ListingsService = Depends(get_listings_service),
):
    """
    Create a new listing for a machine the current user owns.
    Ownership is validated in the service layer by checking machine.customer_id.
    """
    try:
        return service.create_listing(customer_id=user.customer_id, payload=listing)
    except ValueError as e:
        msg = str(e).lower()
        if "machine not found" in msg:
            raise HTTPException(status_code=404, detail="Machine not found")
        if "do not own" in msg or "not allowed" in msg:
            raise HTTPException(status_code=403, detail="Not allowed")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ListingRead])
def list_listings(service: ListingsService = Depends(get_listings_service)):
    """Public listings endpoint."""
    return service.list_listings()


@router.get("/{listing_id:uuid}", response_model=ListingRead)
def get_listing_by_id(
    listing_id: UUID,
    service: ListingsService = Depends(get_listings_service),
):
    try:
        return service.get_listing_by_id(listing_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Listing not found")

