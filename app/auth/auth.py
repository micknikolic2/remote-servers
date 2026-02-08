
from __future__ import annotations

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.service import AuthService, get_auth_service
from app.config import settings
from app.database import get_db
from app.users import UsersRepository

security = HTTPBearer(auto_error=False)

# Enforces that the authenticated user must have one of the specified roles
# bypassed for testing purposes, intended for checking that role is one of the defined ones
def require_roles(*roles):
    def dependency(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return user
    return dependency

# Extracts a token from Authorization header or from cookies
# helper function, used by functions below
def extract_token(credentials: HTTPAuthorizationCredentials, request: Request) -> str | None:
    if credentials and credentials.credentials:
        return credentials.credentials

    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token

    return None

# user authentication, used each time when enpoint is called
def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
    db: Session = Depends(get_db),
):
    users_repo = UsersRepository()

    if not credentials:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = credentials.credentials

    users_repo = UsersRepository()


    # DEVELOPMENT PURPOSES BYPASS (hardcoded dummy user for hardcoded Bearer token)
    if token == settings.DEV_BEARER_TOKEN:
        return users_repo.get_or_create_by_email(
            db=db,
            email=settings.DEV_USER_EMAIL,
        )

    # NORMAL AUTH FLOW
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        user = auth_service.get_current_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user

# check whether token is valid, intended for public endpoints (home page, etc)
def optional_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
):
    token = extract_token(credentials, request)

    try:
        return auth_service.get_current_user(token)
    except Exception:
        return None
