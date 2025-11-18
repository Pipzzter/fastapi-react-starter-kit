import pytest


@pytest.mark.asyncio
async def test_register_and_login(api_client):
    payload = {
        "email": "auth@example.com",
        "password": "secret",
        "full_name": "Auth User",
    }
    response = await api_client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    access_token = response.json()["access_token"]
    assert access_token

    form_data = {"username": payload["email"], "password": payload["password"]}
    response = await api_client.post("/api/v1/auth/token", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
