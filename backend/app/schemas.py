# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Complaint Schemas 

class ComplaintCreate(BaseModel):
    """Schema for creating a new complaint"""
    customer_name: Optional[str] = Field(None, max_length=120)
    email: Optional[EmailStr] = None
    text: str = Field(..., min_length=10, description="Complaint description")

class ComplaintResponse(BaseModel):
    """Complete complaint response"""
    id: int
    customer_name: Optional[str]
    email: Optional[str]
    text: str
    category: Optional[str]
    severity: Optional[str]
    status: str
    notes: Optional[str]
    draft_reply: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth Schemas 

class UserCreate(BaseModel):
    """Create new admin user"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = "admin"

class UserLogin(BaseModel):
    """User login with email and password"""
    email: EmailStr
    password: str

class AdminLoginRequest(BaseModel):
    """Admin login request (alias for UserLogin)"""
    email: EmailStr
    password: str

class OTPVerify(BaseModel):
    """Verify OTP code"""
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)

class OTPRequest(BaseModel):
    """Request OTP"""
    email: EmailStr

class UserResponse(BaseModel):
    """User response"""
    id: int
    email: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Token response with user info"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class LoginResponse(BaseModel):
    """Login response"""
    message: str
    requires_otp: bool = True
    email: Optional[str] = None