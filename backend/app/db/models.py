"""
Database models for the Dermatology AI Assistant.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Boolean, ForeignKey, Text, Date, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from backend.app.db.session import Base


class UserRole(str, enum.Enum):
    """User roles enumeration."""
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class DiagnosisStatus(str, enum.Enum):
    """Diagnosis status enumeration."""
    PENDING_REVIEW = "pending_review"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.PATIENT, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to patient profile
    patient_profile = relationship("Patient", back_populates="user", uselist=False)


class Patient(Base):
    """Patient profile model."""
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    date_of_birth = Column(Date)
    gender = Column(String(20))
    skin_type = Column(String(50))  # Fitzpatrick I-VI
    phone_number = Column(String(20))
    address = Column(Text)
    medical_history = Column(JSON, default=dict)
    family_history = Column(JSON, default=dict)
    allergies = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="patient_profile")
    diagnoses = relationship("Diagnosis", back_populates="patient")
    medical_images = relationship("MedicalImage", back_populates="patient")


class MedicalImage(Base):
    """Medical image model."""
    __tablename__ = "medical_images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    image_path = Column(String, nullable=False)
    body_location = Column(String(100))
    capture_date = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, default=dict)  # camera, lighting, quality scores
    quality_score = Column(Float)
    is_baseline = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="medical_images")
    diagnoses = relationship("Diagnosis", back_populates="image")
    baseline_comparisons = relationship(
        "ImageComparison",
        foreign_keys="ImageComparison.baseline_image_id",
        back_populates="baseline_image"
    )
    followup_comparisons = relationship(
        "ImageComparison",
        foreign_keys="ImageComparison.followup_image_id",
        back_populates="followup_image"
    )


class Diagnosis(Base):
    """Diagnosis model for AI predictions and clinical notes."""
    __tablename__ = "diagnoses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    image_id = Column(UUID(as_uuid=True), ForeignKey("medical_images.id"), nullable=False)
    diagnosis_type = Column(String(50), default="dermatology")
    
    # AI Prediction
    primary_prediction = Column(String(100))
    confidence_score = Column(Float)
    all_predictions = Column(JSON, default=list)
    ensemble_consensus = Column(Boolean)
    
    # Clinical Analysis
    abcde_scores = Column(JSON, default=dict)
    skin_tone = Column(String(50))
    body_location = Column(String(100))
    lesion_diameter_mm = Column(Float)
    
    # Risk Assessment
    risk_assessment = Column(JSON, default=dict)
    risk_level = Column(String(20))  # low, medium, high
    melanoma_risk_score = Column(Float)
    
    # Visualization
    gradcam_path = Column(String)
    segmentation_mask_path = Column(String)
    
    # Clinical Notes
    doctor_notes = Column(Text)
    recommendation = Column(Text)
    status = Column(SQLEnum(DiagnosisStatus), default=DiagnosisStatus.PENDING_REVIEW)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviewed_at = Column(DateTime)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    patient = relationship("Patient", back_populates="diagnoses")
    image = relationship("MedicalImage", back_populates="diagnoses")


class ImageComparison(Base):
    """Image comparison model for tracking lesion changes over time."""
    __tablename__ = "image_comparisons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    baseline_image_id = Column(UUID(as_uuid=True), ForeignKey("medical_images.id"), nullable=False)
    followup_image_id = Column(UUID(as_uuid=True), ForeignKey("medical_images.id"), nullable=False)
    days_between = Column(Integer)
    growth_detected = Column(Boolean, default=False)
    change_score = Column(Float)
    change_analysis = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    baseline_image = relationship("MedicalImage", foreign_keys=[baseline_image_id], back_populates="baseline_comparisons")
    followup_image = relationship("MedicalImage", foreign_keys=[followup_image_id], back_populates="followup_comparisons")


class ChatHistory(Base):
    """Chat history for patient-AI conversations."""
    __tablename__ = "chat_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    context = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    """Audit log for HIPAA compliance."""
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(UUID(as_uuid=True))
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
