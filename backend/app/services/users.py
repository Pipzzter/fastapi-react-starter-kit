from typing import List, Union

from app.models import user as user_models
from app.schemas.user import UserCreate, UserRead
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(
        self, email: Union[str, EmailStr]
    ) -> user_models.User | None:
        result = await self.session.execute(
            select(user_models.User).where(user_models.User.email == str(email))
        )
        return result.scalar_one_or_none()

    async def create_user(
        self, payload: UserCreate, *, hashed_password: str | None = None
    ) -> UserRead:
        password_value = hashed_password or payload.password
        user = user_models.User(
            email=payload.email,
            hashed_password=password_value,
            full_name=payload.full_name,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserRead.model_validate(user)

    async def list_users(self) -> List[UserRead]:
        result = await self.session.execute(select(user_models.User))
        return [UserRead.model_validate(user) for user in result.scalars().all()]
