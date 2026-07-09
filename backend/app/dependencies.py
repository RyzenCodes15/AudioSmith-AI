"""
AudioSmith AI — Dependency Injection.

FastAPI dependency functions for injecting services, repositories,
and database sessions into route handlers.
"""

from __future__ import annotations

from typing import Annotated, AsyncGenerator

from fastapi import Depends

from app.config import Settings, get_settings

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.db.session import create_session_factory
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.core.exceptions import AuthenticationError
from app.core.security import decode_token
from app.models.user import User

# Type alias for injecting settings
SettingsDep = Annotated[Settings, Depends(get_settings)]

async_session_factory = create_session_factory()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ── Database Session ─────────────────────────────────────────────────────

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session per request."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


# ── Repository Dependencies ─────────────────────────────────────────────

async def get_user_repository(session: DbSessionDep) -> UserRepository:
    return UserRepository(session)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]


# ── Service Dependencies ────────────────────────────────────────────────

async def get_auth_service(
    user_repo: UserRepoDep,
    settings: SettingsDep,
) -> AuthService:
    return AuthService(user_repo, settings)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


# ── Authentication ──────────────────────────────────────────────────────

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: UserRepoDep,
) -> User:
    """Validate token and return current user."""
    try:
        payload = decode_token(token)
        user_id: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")
        
        if user_id is None or token_type != "access":
            raise AuthenticationError("Invalid authentication credentials.")
            
    except JWTError as e:
        raise AuthenticationError("Could not validate credentials.") from e

    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise AuthenticationError("User not found.")
        
    if not user.is_active:
        raise AuthenticationError("Inactive user.")
        
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]
