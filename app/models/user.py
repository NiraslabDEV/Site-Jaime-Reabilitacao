from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """User model."""
    id: str
    email: EmailStr
    hashed_password: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """User creation model."""
    email: EmailStr
    password: str


class UserInDB(User):
    """User in database model."""
    pass


