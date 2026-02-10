"""
Dermatology analysis schemas.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class ABCDEScore(BaseModel):
    """ABCDE rule analysis scores."""
    asymmetry: float
    border: float
    color: float
    diameter_mm: float
    evolution: Optional[str] = "unknown"


class ClinicalAnalysis(BaseModel):
    """Clinical analysis results."""
    abcde_score: ABCDEScore
    skin_tone: str
    body_location: Optional[str] = None


class DiagnosisResult(BaseModel):
    """Diagnosis prediction results."""
    primary_prediction: str
    confidence: float
    all_predictions: List[Dict[str, Any]]
    ensemble_consensus: Optional[bool] = None


class VisualizationPaths(BaseModel):
    """Paths to visualization files."""
    gradcam_path: Optional[str] = None
    segmentation_mask: Optional[str] = None


class RiskAssessment(BaseModel):
    """Risk assessment results."""
    overall_risk: str  # low, medium, high
    melanoma_risk_score: float
    risk_factors: List[str]
    protective_factors: List[str]
    recommendation: str


class DermatologyAnalysisResponse(BaseModel):
    """Complete dermatology analysis response."""
    diagnosis: DiagnosisResult
    clinical_analysis: ClinicalAnalysis
    visualization: VisualizationPaths
    risk_assessment: Optional[RiskAssessment] = None
    recommendation: str


class DiagnosisResponse(BaseModel):
    """Database diagnosis record response."""
    id: uuid.UUID
    patient_id: uuid.UUID
    image_id: uuid.UUID
    primary_prediction: str
    confidence_score: float
    all_predictions: List[Dict[str, Any]]
    risk_level: Optional[str]
    recommendation: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ImageComparisonResponse(BaseModel):
    """Image comparison response."""
    id: uuid.UUID
    baseline_image_id: uuid.UUID
    followup_image_id: uuid.UUID
    days_between: int
    growth_detected: bool
    change_score: float
    change_analysis: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True
