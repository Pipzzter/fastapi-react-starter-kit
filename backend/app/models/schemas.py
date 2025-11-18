from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int
    exp: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str
