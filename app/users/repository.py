
from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from .models import User


class UsersRepository:
    def get(self, db: Session, user_id: UUID) -> Optional[User]:
        return db.get(User, user_id)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(
        self,
        db: Session,
        email: str,
        organization_name: str | None = None,
        is_billing_account: bool = False,
    ) -> User:
        new_user = User(
            email=email,
            organization_name=organization_name,
            is_billing_account=is_billing_account,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_or_create_by_email(
        self,
        db: Session,
        email: str,
        organization_name: str | None = None,
        is_billing_account: bool = False,
    ) -> User:
        user = self.get_by_email(db, email)
        if user:
            return user
        return self.create(
            db,
            email=email,
            organization_name=organization_name,
            is_billing_account=is_billing_account,
        )
