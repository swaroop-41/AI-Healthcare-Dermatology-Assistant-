"""
CRUD operations for database models.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, date
import uuid

from backend.app.db.models import User, Patient, MedicalImage, Diagnosis, ImageComparison, UserRole, DiagnosisStatus
from backend.app.core.security import get_password_hash


# User CRUD
def create_user(db: Session, email: str, password: str, full_name: str, role: UserRole = UserRole.PATIENT) -> User:
    """Create a new user."""
    hashed_password = get_password_hash(password)
    user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: uuid.UUID) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


# Patient CRUD
def create_patient(
    db: Session,
    user_id: uuid.UUID,
    date_of_birth: Optional[date] = None,
    gender: Optional[str] = None,
    skin_type: Optional[str] = None,
    phone_number: Optional[str] = None,
    address: Optional[str] = None
) -> Patient:
    """Create a patient profile."""
    patient = Patient(
        user_id=user_id,
        date_of_birth=date_of_birth,
        gender=gender,
        skin_type=skin_type,
        phone_number=phone_number,
        address=address
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patient_by_user_id(db: Session, user_id: uuid.UUID) -> Optional[Patient]:
    """Get patient profile by user ID."""
    return db.query(Patient).filter(Patient.user_id == user_id).first()


def get_patient_history(db: Session, patient_id: uuid.UUID) -> List[Diagnosis]:
    """Get patient diagnosis history."""
    return db.query(Diagnosis).filter(Diagnosis.patient_id == patient_id).order_by(Diagnosis.created_at.desc()).all()


# Medical Image CRUD
def create_medical_image(
    db: Session,
    patient_id: uuid.UUID,
    image_path: str,
    body_location: Optional[str] = None,
    metadata: Optional[dict] = None,
    quality_score: Optional[float] = None,
    is_baseline: bool = False
) -> MedicalImage:
    """Create a medical image record."""
    image = MedicalImage(
        patient_id=patient_id,
        image_path=image_path,
        body_location=body_location,
        metadata=metadata or {},
        quality_score=quality_score,
        is_baseline=is_baseline
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def get_medical_image(db: Session, image_id: uuid.UUID) -> Optional[MedicalImage]:
    """Get medical image by ID."""
    return db.query(MedicalImage).filter(MedicalImage.id == image_id).first()


def get_patient_images(db: Session, patient_id: uuid.UUID) -> List[MedicalImage]:
    """Get all images for a patient."""
    return db.query(MedicalImage).filter(MedicalImage.patient_id == patient_id).order_by(MedicalImage.capture_date.desc()).all()


# Diagnosis CRUD
def create_diagnosis(
    db: Session,
    patient_id: uuid.UUID,
    image_id: uuid.UUID,
    primary_prediction: str,
    confidence_score: float,
    all_predictions: List[dict],
    **kwargs
) -> Diagnosis:
    """Create a diagnosis record."""
    diagnosis = Diagnosis(
        patient_id=patient_id,
        image_id=image_id,
        primary_prediction=primary_prediction,
        confidence_score=confidence_score,
        all_predictions=all_predictions,
        **kwargs
    )
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)
    return diagnosis


def get_diagnosis(db: Session, diagnosis_id: uuid.UUID) -> Optional[Diagnosis]:
    """Get diagnosis by ID."""
    return db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()


def update_diagnosis_status(
    db: Session,
    diagnosis_id: uuid.UUID,
    status: DiagnosisStatus,
    doctor_notes: Optional[str] = None,
    reviewed_by: Optional[uuid.UUID] = None
) -> Optional[Diagnosis]:
    """Update diagnosis status and notes."""
    diagnosis = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
    if diagnosis:
        diagnosis.status = status
        if doctor_notes:
            diagnosis.doctor_notes = doctor_notes
        if reviewed_by:
            diagnosis.reviewed_by = reviewed_by
            diagnosis.reviewed_at = datetime.utcnow()
        db.commit()
        db.refresh(diagnosis)
    return diagnosis


# Image Comparison CRUD
def create_image_comparison(
    db: Session,
    patient_id: uuid.UUID,
    baseline_image_id: uuid.UUID,
    followup_image_id: uuid.UUID,
    days_between: int,
    growth_detected: bool,
    change_score: float,
    change_analysis: Optional[dict] = None
) -> ImageComparison:
    """Create an image comparison record."""
    comparison = ImageComparison(
        patient_id=patient_id,
        baseline_image_id=baseline_image_id,
        followup_image_id=followup_image_id,
        days_between=days_between,
        growth_detected=growth_detected,
        change_score=change_score,
        change_analysis=change_analysis or {}
    )
    db.add(comparison)
    db.commit()
    db.refresh(comparison)
    return comparison


def get_image_comparisons(db: Session, patient_id: uuid.UUID) -> List[ImageComparison]:
    """Get all image comparisons for a patient."""
    return db.query(ImageComparison).filter(ImageComparison.patient_id == patient_id).order_by(ImageComparison.created_at.desc()).all()


def compare_images_timeline(db: Session, patient_id: uuid.UUID, body_location: Optional[str] = None) -> List[MedicalImage]:
    """Get images for timeline comparison."""
    query = db.query(MedicalImage).filter(MedicalImage.patient_id == patient_id)
    if body_location:
        query = query.filter(MedicalImage.body_location == body_location)
    return query.order_by(MedicalImage.capture_date.asc()).all()


def get_patient_risk_factors(db: Session, patient_id: uuid.UUID) -> dict:
    """Get patient risk factors for assessment."""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        return {}
    
    # Calculate age
    age = None
    if patient.date_of_birth:
        today = date.today()
        age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day))
    
    return {
        "age": age,
        "gender": patient.gender,
        "skin_type": patient.skin_type,
        "family_history": patient.family_history,
        "medical_history": patient.medical_history
    }
