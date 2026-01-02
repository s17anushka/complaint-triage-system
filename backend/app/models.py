# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    """Admin users table"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="admin")
    created_at = Column(DateTime, server_default=func.now())


class OTPVerification(Base):
    """OTP verification for admin login"""
    __tablename__ = "otp_verifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp = Column(String(6), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Complaint(Base):
    """Customer complaints table"""
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(120))
    email = Column(String(255))
    text = Column(Text, nullable=False)
    
    # AI-generated fields
    category = Column(String(80))
    severity = Column(String(20))
    route_to = Column(String(80))
    tags = Column(JSON)
    draft_reply = Column(Text)
    notes = Column(Text)
    
    status = Column(String(30), nullable=False, default="open")
    created_at = Column(DateTime, server_default=func.now())