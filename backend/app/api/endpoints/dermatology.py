"""
Dermatology analysis endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import os
import uuid
import shutil
from typing import Optional

from backend.app.db.base import get_db
from backend.app.db import crud
from backend.app.schemas.dermatology import DermatologyAnalysisResponse, DiagnosisResponse
from backend.app.core.security import get_current_user
from backend.app.core.config import settings
from backend.app.core.logging import get_logger

# ML imports
from backend.app.ml.dermatology.skin_classifier import get_classifier
from backend.app.ml.dermatology.gradcam_plus import create_gradcam_visualization
from backend.app.ml.dermatology.abcde_analyzer import get_abcde_analyzer
from backend.app.ml.dermatology.skin_tone import get_skin_tone_classifier
from backend.app.ml.risk.risk_predictor import get_risk_predictor

logger = get_logger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=DermatologyAnalysisResponse)
async def analyze_skin_lesion(
    file: UploadFile = File(...),
    body_location: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze skin lesion from uploaded image.
    
    Performs:
    - AI classification
    - ABCDE rule analysis
    - Skin tone detection
    - Risk assessment
    - Grad-CAM visualization
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # Save uploaded image
        image_id = str(uuid.uuid4())
        image_ext = os.path.splitext(file.filename)[1]
        image_filename = f"{image_id}{image_ext}"
        image_path = os.path.join(settings.UPLOAD_DIR, image_filename)
        
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Image uploaded: {image_path}")
        
        # Get patient
        patient = crud.get_patient_by_user_id(db, current_user["user_id"])
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient profile not found"
            )
        
        # Save medical image record
        medical_image = crud.create_medical_image(
            db,
            patient_id=patient.id,
            image_path=image_path,
            body_location=body_location
        )
        
        # 1. AI Classification
        classifier = get_classifier()
        prediction = classifier.predict(image_path)
        
        # 2. ABCDE Analysis
        abcde_analyzer = get_abcde_analyzer()
        abcde_scores = abcde_analyzer.analyze(image_path)
        
        # 3. Skin Tone Classification
        skin_tone_classifier = get_skin_tone_classifier()
        skin_tone = skin_tone_classifier.classify(image_path)
        
        # 4. Grad-CAM Visualization
        gradcam_filename = f"gradcam_{image_id}.jpg"
        gradcam_path = os.path.join(settings.HEATMAP_DIR, gradcam_filename)
        
        try:
            image_tensor = classifier.preprocess_image(image_path)
            create_gradcam_visualization(
                classifier.model,
                image_path,
                image_tensor,
                gradcam_path
            )
        except Exception as e:
            logger.warning(f"Grad-CAM generation failed: {e}")
            gradcam_path = None
        
        # 5. Risk Assessment
        patient_data = crud.get_patient_risk_factors(db, patient.id)
        risk_predictor = get_risk_predictor()
        risk_assessment = risk_predictor.assess_risk(
            prediction_class=prediction["primary_prediction"],
            confidence=prediction["confidence"],
            abcde_scores=abcde_scores,
            patient_data=patient_data
        )
        
        # Save diagnosis to database
        diagnosis = crud.create_diagnosis(
            db,
            patient_id=patient.id,
            image_id=medical_image.id,
            primary_prediction=prediction["primary_prediction"],
            confidence_score=prediction["confidence"],
            all_predictions=prediction["all_predictions"],
            ensemble_consensus=prediction.get("ensemble_consensus"),
            abcde_scores=abcde_scores,
            skin_tone=skin_tone,
            body_location=body_location,
            lesion_diameter_mm=abcde_scores.get("diameter_mm"),
            risk_assessment=risk_assessment,
            risk_level=risk_assessment["overall_risk"],
            melanoma_risk_score=risk_assessment["melanoma_risk_score"],
            gradcam_path=gradcam_path,
            recommendation=risk_assessment["recommendation"]
        )
        
        logger.info(f"Diagnosis created: {diagnosis.id}")
        
        # Construct response
        response = {
            "diagnosis": {
                "primary_prediction": prediction["primary_prediction"],
                "confidence": prediction["confidence"],
                "all_predictions": prediction["all_predictions"],
                "ensemble_consensus": prediction.get("ensemble_consensus")
            },
            "clinical_analysis": {
                "abcde_score": abcde_scores,
                "skin_tone": skin_tone,
                "body_location": body_location
            },
            "visualization": {
                "gradcam_path": f"/heatmaps/{gradcam_filename}" if gradcam_path else None,
                "segmentation_mask": None
            },
            "risk_assessment": risk_assessment,
            "recommendation": risk_assessment["recommendation"]
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/diagnoses", response_model=list[DiagnosisResponse])
async def get_patient_diagnoses(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all diagnoses for the current patient."""
    try:
        patient = crud.get_patient_by_user_id(db, current_user["user_id"])
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient profile not found"
            )
        
        diagnoses = crud.get_patient_history(db, patient.id)
        return diagnoses
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting diagnoses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get diagnoses"
        )


@router.get("/diagnoses/{diagnosis_id}", response_model=DiagnosisResponse)
async def get_diagnosis(
    diagnosis_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific diagnosis by ID."""
    try:
        diagnosis = crud.get_diagnosis(db, diagnosis_id)
        if not diagnosis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diagnosis not found"
            )
        
        # Verify ownership
        patient = crud.get_patient_by_user_id(db, current_user["user_id"])
        if not patient or diagnosis.patient_id != patient.id:
            # Check if user is doctor or admin
            if current_user.get("role") not in ["doctor", "admin"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this diagnosis"
                )
        
        return diagnosis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting diagnosis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get diagnosis"
        )
