from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import UserRegister, UserLogin, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """Register a new user."""
    return await AuthService.register_user(user_data)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login user and receive JWT token."""
    return await AuthService.login_user(credentials)


