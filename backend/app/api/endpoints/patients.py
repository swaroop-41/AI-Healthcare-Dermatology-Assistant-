"""
Patient management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.db.base import get_db
from backend.app.db import crud
from backend.app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from backend.app.core.security import get_current_user
from backend.app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/profile", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_patient_profile(
    patient_data: PatientCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update patient profile."""
    try:
        # Check if profile already exists
        existing_patient = crud.get_patient_by_user_id(db, current_user["user_id"])
        
        if existing_patient:
            # Update existing profile
            for key, value in patient_data.dict(exclude_unset=True).items():
                setattr(existing_patient, key, value)
            db.commit()
            db.refresh(existing_patient)
            logger.info(f"Patient profile updated for user: {current_user['user_id']}")
            return existing_patient
        else:
            # Create new profile
            patient = crud.create_patient(
                db,
                user_id=current_user["user_id"],
                date_of_birth=patient_data.date_of_birth,
                gender=patient_data.gender,
                skin_type=patient_data.skin_type,
                phone_number=patient_data.phone_number,
                address=patient_data.address
            )
            # Update additional fields
            patient.medical_history = patient_data.medical_history
            patient.family_history = patient_data.family_history
            patient.allergies = patient_data.allergies
            db.commit()
            db.refresh(patient)
            logger.info(f"Patient profile created for user: {current_user['user_id']}")
            return patient
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error managing patient profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to manage patient profile"
        )


@router.get("/profile", response_model=PatientResponse)
async def get_patient_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current patient profile."""
    try:
        patient = crud.get_patient_by_user_id(db, current_user["user_id"])
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient profile not found"
            )
        return patient
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting patient profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get patient profile"
        )
