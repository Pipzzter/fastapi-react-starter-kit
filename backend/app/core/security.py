from datetime import UTC, datetime, timedelta
from typing import Any, Optional

from app.core.config import get_settings
from jose import JWTError, jwt
from pwdlib import PasswordHash

settings = get_settings()
pwd_hasher = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_hasher.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_hasher.hash(password)


def create_access_token(
    subject: str | int, expires_delta: Optional[timedelta] = None
) -> str:
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode: dict[str, Any] = {"sub": str(subject), "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
