
from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import get_current_user
from app.users import User

from .schemas import BookingRead, BookingRequest
from .service import BookingsService, get_bookings_service

router = APIRouter()


@router.post("/request", response_model=BookingRead)
def request_booking(
    booking: BookingRequest,
    user: User = Depends(get_current_user),
    service: BookingsService = Depends(get_bookings_service),
):
    """
    Create a booking request as the authenticated user (buyer).
    """
    try:
        return service.request_booking(user.customer_id, payload=booking)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[BookingRead])
def list_my_bookings(
    user: User = Depends(get_current_user),
    service: BookingsService = Depends(get_bookings_service),
):
    """
    List bookings of an authenticated user.
    """
    try:
        return service.list_bookings_for_user(user.customer_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))