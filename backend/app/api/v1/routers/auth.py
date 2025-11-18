from app.db.session import get_session
from app.models.schemas import Token, UserCreate
from app.services.auth import AuthService
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate, session: AsyncSession = Depends(get_session)
) -> Token:
    auth_service = AuthService(session)
    user = await auth_service.register_user(payload)
    return auth_service.generate_token(user.id)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> Token:
    auth_service = AuthService(session)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    return auth_service.generate_token(user.id)
