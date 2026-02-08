import jwt
from jwt import PyJWTError
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.users import get_users_public, UsersPublic
from app.users import User
from app.config import settings
from app.database import get_db

# Bridges Supabase authentication with the internal User domain
# Handles decoding tokens, parsing mock tokens, and provisioning userss
class AuthService:
    def __init__(self, db: Session, users_public: UsersPublic):
        self.db = db
        self.supabase_jwt_secret = settings.SUPABASE_JWT_SECRET
        self.users_public = users_public
        
    # helper method for decoding JWI (HS256 with SUPABASE_JWT_SECRET)
    def _decode_supabase_jwt(self, token: str) -> dict:
        if not self.supabase_jwt_secret:
            raise RuntimeError("SUPABASE_JWT_SECRET not set.")

        try:
            return jwt.decode(
                token,
                self.supabase_jwt_secret,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
        except PyJWTError as e:
            raise ValueError(f"Invalid or expired JWT: {str(e)}")

    # helper method, propagating call to users service, used from the method down below
    def _get_or_create_user(
            self, sub: str, email: Optional[str], role: Optional[str]
        ) -> User:
            if not email:
                raise ValueError("Missing email for user provisioning")

            return self.users_public.get_or_create_by_email(email=email)

    # returns the authenticated user or None, if no token was provided
    # token validation, used from auth.py, on each endpoint call
    def get_current_user(self, token: Optional[str]) -> Optional[User]:
        if not token:
            return None

        token = token.strip()

        if token.lower().startswith("bearer "):
            token = token[7:].strip()

        #Real Supabase JWT
        payload = self._decode_supabase_jwt(token)

        sub = payload.get("sub")
        #handle Supabase email nesting in user_metadata
        email = payload.get("email") or payload.get("user_metadata", {}).get("email")
        metadata = payload.get("user_metadata") or {}
        role = metadata.get("role")

        if not sub or not email:
            raise ValueError("Invalid JWT payload: missing 'sub' or 'email'.")

        return self._get_or_create_user(sub=sub, email=email, role=role)


def get_auth_service(
    db: Session = Depends(get_db),
    users_public: UsersPublic = Depends(get_users_public)
) -> AuthService:
    return AuthService(db, users_public)