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

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(payload: RegisterRequest) -> UserResponse:
    """Register a new user account."""
    # Future: delegate to AuthService
    raise NotImplementedError("Registration not yet implemented.")


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    """Authenticate user and return JWT tokens."""
    # Future: delegate to AuthService
    raise NotImplementedError("Login not yet implemented.")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token() -> TokenResponse:
    """Refresh an expired access token using a valid refresh token."""
    # Future: delegate to AuthService
    raise NotImplementedError("Token refresh not yet implemented.")


@router.get("/me", response_model=UserResponse)
async def get_current_user() -> UserResponse:
    """Get the current authenticated user's profile."""
    # Future: delegate to AuthService
    raise NotImplementedError("Profile access not yet implemented.")
