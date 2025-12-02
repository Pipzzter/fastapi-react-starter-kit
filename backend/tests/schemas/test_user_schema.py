import pytest
from app.schemas.user import UserCreate, UserLogin, UserRead
from pydantic import ValidationError
from pydantic.v1 import EmailStr


class _UserRecord:
    """Simple object to emulate ORM model for from_attributes tests."""

    def __init__(self, *, id: int, email: str, full_name: str | None):
        self.id = id
        self.email = email
        self.full_name = full_name


def test_user_create_valid_payload():
    payload = UserCreate(
        email=EmailStr("demo@example.com"), full_name="Demo", password="secret"
    )

    assert payload.email == "demo@example.com"
    assert payload.full_name == "Demo"
    assert payload.password == "secret"


def test_user_create_missing_email_raises():
    with pytest.raises(ValidationError):
        UserCreate(full_name="Demo", password="secret")


def test_user_create_missing_password_raises():
    with pytest.raises(ValidationError):
        UserCreate(email=EmailStr("demo@example.com"))


def test_user_read_from_attributes_object():
    record = _UserRecord(id=1, email=EmailStr("demo@example.com"), full_name="Demo")

    result = UserRead.model_validate(record)

    assert result.id == 1
    assert result.email == "demo@example.com"
    assert result.full_name == "Demo"


def test_user_read_invalid_id_type_raises():
    with pytest.raises(ValidationError):
        UserRead(id="one", email=EmailStr("demo@example.com"), full_name=None)


def test_user_login_validates_email_format():
    login = UserLogin(email=EmailStr("demo@example.com"), password="secret")

    assert login.email == "demo@example.com"
    assert login.password == "secret"


def test_user_login_invalid_email_raises():
    with pytest.raises(ValidationError):
        UserLogin(email=EmailStr("not-an-email"), password="secret")
