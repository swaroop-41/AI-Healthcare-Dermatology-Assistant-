"""
Report generation endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from backend.app.db.base import get_db
from backend.app.db import crud
from backend.app.core.security import get_current_user
from backend.app.core.logging import get_logger
from backend.app.services.pdf_generator import get_pdf_generator

logger = get_logger(__name__)
router = APIRouter()


@router.get("/generate/{diagnosis_id}")
async def generate_pdf_report(
    diagnosis_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate PDF report for a diagnosis."""
    try:
        # Get diagnosis
        diagnosis = crud.get_diagnosis(db, diagnosis_id)
        if not diagnosis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diagnosis not found"
            )
        
        # Verify ownership or role
        patient = crud.get_patient_by_user_id(db, current_user["user_id"])
        if patient and diagnosis.patient_id != patient.id:
            if current_user.get("role") not in ["doctor", "admin"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this diagnosis"
                )
        
        # Get patient info
        patient_obj = db.query(crud.Patient).filter(crud.Patient.id == diagnosis.patient_id).first()
        user_obj = db.query(crud.User).filter(crud.User.id == patient_obj.user_id).first()
        
        patient_info = {
            "name": user_obj.full_name if user_obj else "N/A",
            "date_of_birth": patient_obj.date_of_birth if patient_obj else None,
            "gender": patient_obj.gender if patient_obj else "N/A",
            "skin_type": patient_obj.skin_type if patient_obj else "N/A"
        }
        
        # Prepare diagnosis data
        diagnosis_data = {
            "id": str(diagnosis.id),
            "diagnosis": {
                "primary_prediction": diagnosis.primary_prediction,
                "confidence": diagnosis.confidence_score,
                "all_predictions": diagnosis.all_predictions
            },
            "abcde_scores": diagnosis.abcde_scores,
            "risk_level": diagnosis.risk_level,
            "recommendation": diagnosis.recommendation,
            "gradcam_path": diagnosis.gradcam_path
        }
        
        # Generate PDF
        pdf_generator = get_pdf_generator()
        pdf_path = pdf_generator.generate_report(
            diagnosis_data=diagnosis_data,
            patient_info=patient_info,
            output_filename=f"report_{diagnosis_id}.pdf"
        )
        
        # Return file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"dermatology_report_{diagnosis_id}.pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate PDF report"
        )
