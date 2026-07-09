"""
AudioSmith AI — Security Utilities.

JWT token creation/verification and password hashing.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings

# ── Password Hashing ────────────────────────────────────────────────────

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT Tokens ──────────────────────────────────────────────────────────


def create_access_token(
    subject: str,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Create a JWT access token.

    Args:
        subject: The token subject (typically user ID).
        extra_claims: Additional claims to include in the token.

    Returns:
        Encoded JWT string.
    """
    settings = get_settings()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expire,
        "type": "access",
        **(extra_claims or {}),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(subject: str) -> str:
    """Create a JWT refresh token.

    Args:
        subject: The token subject (typically user ID).

    Returns:
        Encoded JWT string.
    """
    settings = get_settings()

    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.jwt_refresh_token_expire_days
    )

    payload = {
        "sub": subject,
        "exp": expire,
        "type": "refresh",
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_token(token: str) -> dict[str, Any]:
    """Decode and verify a JWT token.

    Args:
        token: The JWT string to decode.

    Returns:
        Decoded token payload.

    Raises:
        JWTError: If the token is invalid or expired.
    """
    settings = get_settings()

    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
