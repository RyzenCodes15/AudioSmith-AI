"""
AudioSmith AI — Dependency Injection.

FastAPI dependency functions for injecting services, repositories,
and database sessions into route handlers.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.core.exceptions import AuthenticationError
from app.core.security import decode_token
from app.db.session import create_session_factory
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.audio_repository import AudioRepository
from app.repositories.job_repository import JobRepository
from app.services.auth_service import AuthService
from app.services.audio_service import AudioService
from app.services.storage.base import StorageBackend
from app.services.storage.local import LocalStorageBackend

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
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


# ── Repository Dependencies ─────────────────────────────────────────────

async def get_user_repository(session: DbSessionDep) -> UserRepository:
    return UserRepository(session)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]

async def get_audio_repository(session: DbSessionDep) -> AudioRepository:
    return AudioRepository(session)

AudioRepoDep = Annotated[AudioRepository, Depends(get_audio_repository)]

async def get_job_repository(session: DbSessionDep) -> JobRepository:
    return JobRepository(session)

JobRepoDep = Annotated[JobRepository, Depends(get_job_repository)]

# ── Service Dependencies ────────────────────────────────────────────────

async def get_auth_service(
    user_repo: UserRepoDep,
    settings: SettingsDep,
) -> AuthService:
    return AuthService(user_repo, settings)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_storage_backend(settings: SettingsDep) -> StorageBackend:
    if settings.storage_backend == "local":
        return LocalStorageBackend(base_path=settings.storage_local_path)
    # Future: return S3StorageBackend(...)
    raise NotImplementedError(f"Storage backend {settings.storage_backend} not implemented")

StorageBackendDep = Annotated[StorageBackend, Depends(get_storage_backend)]

async def get_audio_service(
    audio_repo: AudioRepoDep,
    job_repo: JobRepoDep,
    storage: StorageBackendDep,
    settings: SettingsDep,
) -> AudioService:
    return AudioService(audio_repo, job_repo, storage, settings)

AudioServiceDep = Annotated[AudioService, Depends(get_audio_service)]

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
