from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock

import pytest
import pytest_asyncio
from app.api.v1.routers import auth as auth_router
from app.api.v1.routers import health as health_router
from app.api.v1.routers import user as user_router


@pytest.fixture
def mock_user_service(monkeypatch):
    service = Mock()
    service.get_by_email = AsyncMock(return_value=None)
    service.create_user = AsyncMock(return_value=None)
    service.list_users = AsyncMock(return_value=[])
    monkeypatch.setattr(user_router, "UserService", lambda session: service)
    return service


@pytest.fixture
def mock_auth_service(monkeypatch):
    service = Mock()
    service.register_user = AsyncMock()
    service.authenticate_user = AsyncMock()
    service.generate_token = Mock()
    monkeypatch.setattr(auth_router, "AuthService", lambda session: service)
    return service


@pytest.fixture
def mock_health_service(monkeypatch):
    service = Mock()
    service.get_status = AsyncMock(
        return_value={
            "status": "ok",
            "timestamp": datetime.now(timezone.utc),
        }
    )
    monkeypatch.setattr(health_router, "HealthService", lambda: service)
    return service


@pytest_asyncio.fixture()
async def async_client(api_client):
    yield api_client
