"""
AudioSmith AI — Authentication Endpoints.

Handles user registration, login, token refresh, and profile access.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.dependencies import AuthServiceDep, CurrentUserDep
from app.models.user import User
from pydantic import BaseModel

class RefreshRequest(BaseModel):
    refresh_token: str


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(payload: RegisterRequest, auth_service: AuthServiceDep) -> dict:
    """Register a new user account."""
    return await auth_service.register(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, auth_service: AuthServiceDep) -> dict:
    """Authenticate user and return JWT tokens."""
    return await auth_service.login(email=payload.email, password=payload.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(payload: RefreshRequest, auth_service: AuthServiceDep) -> dict:
    """Refresh an expired access token using a valid refresh token."""
    return await auth_service.refresh_token(payload.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: CurrentUserDep) -> User:
    """Get the current authenticated user's profile."""
    return current_user

@router.post("/logout")
async def logout(current_user: CurrentUserDep) -> dict:
    """Logout endpoint. For JWTs stored in localStorage, client clears it."""
    return {"message": "Successfully logged out"}
