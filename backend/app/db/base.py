"""
Base database imports and initialization.
"""

from backend.app.db.session import Base, engine, get_db
from backend.app.db.models import (
    User,
    Patient,
    MedicalImage,
    Diagnosis,
    ImageComparison,
    ChatHistory,
    AuditLog,
    UserRole,
    DiagnosisStatus
)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


__all__ = [
    "Base",
    "engine",
    "get_db",
    "init_db",
    "User",
    "Patient",
    "MedicalImage",
    "Diagnosis",
    "ImageComparison",
    "ChatHistory",
    "AuditLog",
    "UserRole",
    "DiagnosisStatus"
]
