from typing import Optional
from app.core.database import supabase
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import UserRegister, UserLogin, Token
from app.models.user import User
from fastapi import HTTPException, status


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    async def register_user(user_data: UserRegister) -> Token:
        """Register a new user."""
        # Check if user already exists
        existing_user = supabase.table("users").select("id").eq("email", user_data.email).execute()
        
        if existing_user.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create user in Supabase
        new_user = supabase.table("users").insert({
            "email": user_data.email,
            "hashed_password": hashed_password
        }).execute()
        
        if not new_user.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        user_id = new_user.data[0]["id"]
        
        # Generate JWT token
        access_token = create_access_token(data={"sub": user_id})
        
        return Token(access_token=access_token)
    
    @staticmethod
    async def login_user(credentials: UserLogin) -> Token:
        """Authenticate user and return JWT token."""
        # Get user from database
        user_result = supabase.table("users").select("*").eq("email", credentials.email).execute()
        
        if not user_result.data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        user = user_result.data[0]
        
        # Verify password
        if not verify_password(credentials.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Generate JWT token
        access_token = create_access_token(data={"sub": user["id"]})
        
        return Token(access_token=access_token)
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user by ID."""
        user_result = supabase.table("users").select("*").eq("id", user_id).execute()
        
        if not user_result.data:
            return None
        
        user_data = user_result.data[0]
        return User(**user_data)


