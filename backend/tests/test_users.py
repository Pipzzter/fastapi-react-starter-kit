import pytest
from app.models.schemas import UserCreate
from app.services.users import UserService
from pydantic import EmailStr, TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

email_adapter = TypeAdapter(EmailStr)


def make_email(value: str) -> EmailStr:
    return email_adapter.validate_python(value)


@pytest.mark.asyncio
async def test_create_user(api_client, db_session: AsyncSession):
    payload = UserCreate(
        email=make_email("user@example.com"), password="secret", full_name="Test User"
    )
    response = await api_client.post("/api/v1/users/", json=payload.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload.email

    service = UserService(db_session)
    user = await service.get_by_email(payload.email)
    assert user is not None
    assert user.full_name == payload.full_name


@pytest.mark.asyncio
async def test_list_users(api_client):
    payload = UserCreate(
        email=make_email("another@example.com"),
        password="secret",
        full_name="Another User",
    )
    await api_client.post("/api/v1/users/", json=payload.model_dump())
    response = await api_client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["email"] == payload.email for item in data)
