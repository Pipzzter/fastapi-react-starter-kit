from types import SimpleNamespace

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_register_user_router(async_client, mock_auth_service):
    payload = {
        "email": "auth@example.com",
        "password": "secret",
        "full_name": "Auth User",
    }
    mock_auth_service.register_user.return_value = SimpleNamespace(id=1)
    mock_auth_service.generate_token.return_value = {
        "access_token": "token",
        "token_type": "bearer",
    }

    response = await async_client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == mock_auth_service.generate_token.return_value
    mock_auth_service.register_user.assert_awaited_once()
    mock_auth_service.generate_token.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_login_router(async_client, mock_auth_service):
    mock_auth_service.authenticate_user.return_value = SimpleNamespace(id=2)
    mock_auth_service.generate_token.return_value = {
        "access_token": "token",
        "token_type": "bearer",
    }

    response = await async_client.post(
        "/api/v1/auth/token",
        data={"username": "auth@example.com", "password": "secret"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_auth_service.generate_token.return_value
    mock_auth_service.authenticate_user.assert_awaited_once_with(
        "auth@example.com", "secret"
    )
    mock_auth_service.generate_token.assert_called_once_with(2)
