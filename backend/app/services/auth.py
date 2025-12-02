from datetime import timedelta
from typing import Optional

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models import user as user_models
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead
from app.services.users import UserService
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_service = UserService(session)

    async def authenticate_user(self, email: str, password: str) -> user_models.User:
        user = await self.user_service.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        return user

    async def register_user(self, payload: UserCreate) -> UserRead:
        user = await self.user_service.get_by_email(payload.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        hashed_password = get_password_hash(payload.password)
        return await self.user_service.create_user(
            payload, hashed_password=hashed_password
        )

    @staticmethod
    def generate_token(
        user_id: int, expires_delta: Optional[timedelta] = None
    ) -> Token:
        token = create_access_token(user_id, expires_delta)
        return Token(access_token=token, token_type="bearer")
