"""
AudioSmith AI — Dependency Injection.

FastAPI dependency functions for injecting services, repositories,
and database sessions into route handlers.
"""

from __future__ import annotations

from typing import Annotated, AsyncGenerator

from fastapi import Depends

from app.config import Settings, get_settings

# Type alias for injecting settings
SettingsDep = Annotated[Settings, Depends(get_settings)]


# ── Database Session ─────────────────────────────────────────────────────
# Future: uncomment when database is configured
#
# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     """Yield a database session per request."""
#     async with async_session_factory() as session:
#         try:
#             yield session
#         finally:
#             await session.close()
#
# DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


# ── Repository Dependencies ─────────────────────────────────────────────
# Future: inject repositories that depend on DbSessionDep
#
# async def get_user_repository(session: DbSessionDep) -> UserRepository:
#     return UserRepository(session)
#
# UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]


# ── Service Dependencies ────────────────────────────────────────────────
# Future: inject services that depend on repositories
#
# async def get_auth_service(
#     user_repo: UserRepoDep,
#     settings: SettingsDep,
# ) -> AuthService:
#     return AuthService(user_repo, settings)
#
# AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
