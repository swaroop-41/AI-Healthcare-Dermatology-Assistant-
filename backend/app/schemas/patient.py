"""
Patient schemas.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import uuid


class PatientCreate(BaseModel):
    """Schema for creating a patient profile."""
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    skin_type: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[Dict[str, Any]] = {}
    family_history: Optional[Dict[str, Any]] = {}
    allergies: Optional[List[str]] = []


class PatientUpdate(BaseModel):
    """Schema for updating a patient profile."""
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    skin_type: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[Dict[str, Any]] = None
    family_history: Optional[Dict[str, Any]] = None
    allergies: Optional[List[str]] = None


class PatientResponse(BaseModel):
    """Schema for patient response."""
    id: uuid.UUID
    user_id: uuid.UUID
    date_of_birth: Optional[date]
    gender: Optional[str]
    skin_type: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    medical_history: Dict[str, Any]
    family_history: Dict[str, Any]
    allergies: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
