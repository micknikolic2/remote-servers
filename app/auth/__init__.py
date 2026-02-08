"""
Public interface for the Auth domain module.
"""

from .auth import get_current_user, optional_user

__all__ = ["get_current_user", "optional_user"]