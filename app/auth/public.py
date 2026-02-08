from fastapi import Depends, HTTPException, status
from typing import Protocol

from app.users import UsersPublic, get_users_public
from app.auth.auth import get_current_user

# Defines the public authorization interface (Inversion of Control frinedly)
# These checks are placeholders for a future role-based authorization system
class AuthPublic(Protocol):
    def ensure_buyer(self) -> None: 
        pass
    def ensure_provider(self) -> None: 
        pass
    def ensure_admin(self) -> None: 
        pass

# Delegates role checks to UsersPublic
class AuthPublicImpl:
    def __init__(self, current_user, users_public: UsersPublic):
        self.current_user = current_user
        self.users_public = users_public

    def ensure_buyer(self) -> None:
        if not self.users_public.is_buyer(self.current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Buyer role required.",
            )

    def ensure_provider(self) -> None:
        if not self.users_public.is_provider(self.current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provider role required.",
            )

    def ensure_admin(self) -> None:
        if not self.users_public.is_admin(self.current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin role required.",
            )


# Dependency provider for AuthPublic
# Wires together authentication (current user) and authorization checks
def get_auth_public(
    current_user=Depends(get_current_user),
    users_public: UsersPublic = Depends(get_users_public),
) -> AuthPublic:
    return AuthPublicImpl(current_user=current_user, users_public=users_public)

# FastAPI dependency for buyer-only endpoints
def ensure_buyer(auth_public: AuthPublic = Depends(get_auth_public)):
    auth_public.ensure_buyer()
    return auth_public.current_user

# FastAPI dependency for provider-only endpoints
def ensure_provider(auth_public: AuthPublic = Depends(get_auth_public)):
    auth_public.ensure_provider()
    return auth_public.current_user

# FastAPI dependency for admin-only endpoints
def ensure_admin(auth_public: AuthPublic = Depends(get_auth_public)):
    auth_public.ensure_admin()
    return auth_public.current_user
