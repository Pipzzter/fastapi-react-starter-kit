import logging
from typing import List, Union

from app.core.security import get_password_hash
from app.models import user as user_models
from app.schemas.user import UserCreate, UserRead
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: Union[str, str]) -> user_models.User | None:
        result = await self.session.execute(
            select(user_models.User).where(user_models.User.email == str(email))
        )
        user = result.scalar_one_or_none()
        logger.debug("Fetched user by email %s => %s", email, bool(user))
        return user

    async def create_user(
        self, payload: UserCreate, *, hashed_password: str | None = None
    ) -> UserRead:
        password_value = hashed_password or get_password_hash(payload.password)
        user = user_models.User(
            email=payload.email,
            hashed_password=password_value,
            full_name=payload.full_name,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info("Created user %s", user.email)
        return UserRead.model_validate(user)

    async def list_users(self) -> List[UserRead]:
        result = await self.session.execute(select(user_models.User))
        records = [UserRead.model_validate(user) for user in result.scalars().all()]
        logger.debug("List users returned %d records", len(records))
        return records
