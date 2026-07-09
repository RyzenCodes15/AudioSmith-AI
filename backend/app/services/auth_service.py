"""
AudioSmith AI — Authentication Service.

Business logic for user registration, login, and token management.
"""

from __future__ import annotations

from app.config import Settings
from app.core.exceptions import AuthenticationError, ConflictError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import UserRepository


class AuthService:
    """Handles authentication business logic.

    This service orchestrates user registration, login, and token
    operations. It depends on the UserRepository for data access
    and Settings for configuration.
    """

    def __init__(self, user_repo: UserRepository, settings: Settings) -> None:
        self._user_repo = user_repo
        self._settings = settings

    async def register(
        self,
        email: str,
        password: str,
        full_name: str,
    ) -> dict:
        """Register a new user.

        Args:
            email: User's email address.
            password: Plaintext password (will be hashed).
            full_name: User's display name.

        Returns:
            Created user data.

        Raises:
            ConflictError: If email is already registered.
        """
        if await self._user_repo.email_exists(email):
            raise ConflictError(f"Email '{email}' is already registered.")

        hashed = hash_password(password)
        user = await self._user_repo.create(
            email=email,
            hashed_password=hashed,
            full_name=full_name,
        )

        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "created_at": user.created_at,
            "is_active": user.is_active,
        }

    async def login(self, email: str, password: str) -> dict:
        """Authenticate a user and return tokens.

        Args:
            email: User's email address.
            password: Plaintext password.

        Returns:
            Token pair (access + refresh).

        Raises:
            AuthenticationError: If credentials are invalid.
        """
        user = await self._user_repo.get_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationError("Account is deactivated.")

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self._settings.jwt_access_token_expire_minutes * 60,
        }
