import pytest
from app.schemas.user import UserCreate
from app.services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_user(api_client, db_session: AsyncSession):
    payload = UserCreate(
        email="user10@example.com", password="secret", full_name="Test User"
    )
    response = await api_client.post("/api/v1/user/", json=payload.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload.email

    service = UserService(db_session)
    user = await service.get_by_email(payload.email)
    assert user is not None
    assert user.full_name == payload.full_name
    assert user.hashed_password != payload.password


@pytest.mark.asyncio
async def test_list_users(api_client):
    payload = UserCreate(
        email="another@example.com",
        password="secret",
        full_name="Another User",
    )
    await api_client.post("/api/v1/user/", json=payload.model_dump())
    response = await api_client.get("/api/v1/user/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["email"] == payload.email for item in data)


@pytest.mark.asyncio
async def test_create_user_duplicate_email(api_client):
    payload = UserCreate(email="dupe@example.com", password="secret", full_name="Dupe")
    first = await api_client.post("/api/v1/user/", json=payload.model_dump())
    assert first.status_code == 201
    duplicate = await api_client.post("/api/v1/user/", json=payload.model_dump())
    assert duplicate.status_code == 400
    assert duplicate.json()["detail"] == "Email already registered"
