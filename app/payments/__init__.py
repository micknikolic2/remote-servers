"""
Public interface for the Payments domain module.
"""

from .routes import router
from .service import PaymentsService, get_payments_service

__all__ = [
    "router",
    "PaymentsService",
    "get_payments_service",
]
