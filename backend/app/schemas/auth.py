"""
Authentication schemas.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str
    full_name: str
    role: Optional[str] = "patient"


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""
    user_id: Optional[str] = None
    email: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response."""
    id: uuid.UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
