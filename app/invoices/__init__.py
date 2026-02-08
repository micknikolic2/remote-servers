"""
Public interface for the Invoices domain module.
"""

from .service import InvoicesService, get_invoices_service

__all__ = [
    "InvoicesService",
    "get_invoices_service",
]
