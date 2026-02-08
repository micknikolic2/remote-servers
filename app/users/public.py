
from __future__ import annotations

from typing import Protocol, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from .repository import UsersRepository
from .models import User


class UsersPublic(Protocol):
    def get_or_create_by_email(self, email: str) -> User:
        pass

    def get_user(self, user_id: UUID) -> Optional[User]:
        pass

    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    def create_user(
        self,
        email: str,
        organization_name: str | None = None,
        is_billing_account: bool = False,
    ) -> User:
        pass

    def get_or_create_user_by_email(
        self,
        email: str,
        organization_name: str | None = None,
        is_billing_account: bool = False,
    ) -> User:
        pass

    # These methods are placeholders for a real authorization system
    # In a production setup, user roles/permissions would be validated here
    # Currently, this is bypassed by hardcoded token, so the system is intentionally simplified
    def is_buyer(self, user: User) -> bool: 
        pass

    def is_provider(self, user: User) -> bool: 
        pass

    def is_admin(self, user: User) -> bool: 
        pass

class UsersPublicImpl:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UsersRepository()

    def get_or_create_by_email(self, email: str) -> User:
        return self.repo.get_or_create_by_email(self.db, email=email)
    
    def get_user(self, user_id: UUID) -> Optional[User]:
        return self.repo.get(self.db, user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.repo.get_by_email(self.db, email)

    def create_user(
        self,
        email: str,
        organization_name: str | None = None,
        is_billing_account: bool = False,
    ) -> User:
        return self.repo.create(
            self.db,
            email=email,
            organization_name=organization_name,
            is_billing_account=is_billing_account,
        )

    def get_or_create_user_by_email(
        self,
        email: str,
        organization_name: str | None = None,
        is_billing_account: bool = False,
    ) -> User:
        return self.repo.get_or_create_by_email(
            self.db,
            email=email,
            organization_name=organization_name,
            is_billing_account=is_billing_account,
        )
    
    def is_buyer(self, user: User) -> bool:
        return getattr(user, "role", None) == "buyer"

    def is_provider(self, user: User) -> bool:
        return getattr(user, "role", None) == "provider"

    def is_admin(self, user: User) -> bool:
        return getattr(user, "role", None) == "admin"

# Dependency provider wiring the public facade to the implementation
def get_users_public(db: Session = Depends(get_db)) -> UsersPublic:
    return UsersPublicImpl(db)
