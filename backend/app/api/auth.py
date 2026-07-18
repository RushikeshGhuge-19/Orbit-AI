from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.models.user import User
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(UserRepository(db))

    try:
        return await service.register_user(user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get(
    "/me",
    response_model=UserResponse,
)
async def me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(UserRepository(db))

    try:
        return await service.login(
            email=form_data.username,
            password=form_data.password,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )