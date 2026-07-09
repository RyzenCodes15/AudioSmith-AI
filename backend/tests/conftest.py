"""
AudioSmith AI — Test Configuration.

Shared fixtures for backend tests.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import create_app


@pytest.fixture
def app():
    """Create a test FastAPI application."""
    return create_app()


@pytest.fixture
async def client(app):
    """Create an async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
