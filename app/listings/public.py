
from __future__ import annotations

from typing import Protocol
from uuid import UUID
from fastapi import Depends

from .service import ListingsService, get_listings_service
from .schemas import ListingCreate

# Public facade for listing-related operations
class ListingsPublic(Protocol):
    def create_listing(self, customer_id: UUID, payload: ListingCreate):
        pass

    def get_listing_by_id(self, listing_id: UUID):
        pass

    def list_listings(self):
        pass


# Default implementation of ListingsPublic
# Thin adapter layer that forwards calls to the service layer
class ListingsPublicImpl:
    def __init__(self, service: ListingsService):
        self.service = service

    def create_listing(self, customer_id: UUID, payload: ListingCreate):
        return self.service.create_listing(customer_id, payload)

    def get_listing_by_id(self, listing_id: UUID):
        return self.service.get_listing_by_id(listing_id)

    def list_listings(self):
        return self.service.list_listings()


# Dependency provider wiring the public facade to its service implementation
def get_listings_public(service: ListingsService = Depends(get_listings_service)) -> ListingsPublic:
    return ListingsPublicImpl(service)
