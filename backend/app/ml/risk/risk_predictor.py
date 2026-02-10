"""
Risk assessment predictor for dermatology cases.
"""

import numpy as np
from typing import Dict, List, Optional
from datetime import date

from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class RiskPredictor:
    """Predict melanoma and skin cancer risk."""
    
    # Risk thresholds
    LOW_RISK_THRESHOLD = 0.3
    HIGH_RISK_THRESHOLD = 0.7
    
    def __init__(self):
        """Initialize risk predictor."""
        pass
    
    def assess_risk(
        self,
        prediction_class: str,
        confidence: float,
        abcde_scores: Dict[str, float],
        patient_data: Optional[Dict] = None
    ) -> Dict:
        """
        Assess melanoma and overall skin cancer risk.
        
        Args:
            prediction_class: AI predicted class
            confidence: Prediction confidence
            abcde_scores: ABCDE analysis scores
            patient_data: Patient demographic and history data
        
        Returns:
            Risk assessment dictionary
        """
        try:
            # Initialize risk factors and protective factors
            risk_factors = []
            protective_factors = []
            
            # Base melanoma risk from prediction
            melanoma_risk = 0.0
            if prediction_class == "MEL":
                melanoma_risk = confidence
                risk_factors.append(f"AI detected melanoma (confidence: {confidence:.2%})")
            elif prediction_class in ["BCC", "SCC"]:
                melanoma_risk = 0.3  # Moderate baseline for other malignancies
                risk_factors.append(f"AI detected {prediction_class}")
            else:
                melanoma_risk = 0.1  # Low baseline for benign conditions
            
            # ABCDE risk factors
            if abcde_scores:
                if abcde_scores.get('asymmetry', 0) > 0.6:
                    melanoma_risk += 0.1
                    risk_factors.append("High asymmetry score")
                
                if abcde_scores.get('border', 0) > 0.6:
                    melanoma_risk += 0.1
                    risk_factors.append("Irregular border detected")
                
                if abcde_scores.get('color', 0) > 0.7:
                    melanoma_risk += 0.1
                    risk_factors.append("High color variation")
                
                if abcde_scores.get('diameter_mm', 0) > 6:
                    melanoma_risk += 0.15
                    risk_factors.append(f"Lesion diameter > 6mm ({abcde_scores.get('diameter_mm'):.1f}mm)")
            
            # Patient demographic risk factors
            if patient_data:
                age = patient_data.get('age')
                if age and age > 60:
                    melanoma_risk += 0.1
                    risk_factors.append("Age > 60")
                elif age and age < 30:
                    protective_factors.append("Age < 30")
                
                skin_type = patient_data.get('skin_type', '')
                if 'Type I' in skin_type or 'Type II' in skin_type:
                    melanoma_risk += 0.15
                    risk_factors.append("Fair skin (Fitzpatrick Type I-II)")
                
                family_history = patient_data.get('family_history', {})
                if family_history.get('melanoma') or family_history.get('skin_cancer'):
                    melanoma_risk += 0.2
                    risk_factors.append("Family history of melanoma/skin cancer")
                
                medical_history = patient_data.get('medical_history', {})
                if not medical_history.get('smoking'):
                    protective_factors.append("Non-smoker")
                if medical_history.get('regular_skin_checks'):
                    protective_factors.append("Regular skin checks")
            
            # Cap risk score at 1.0
            melanoma_risk = min(melanoma_risk, 1.0)
            
            # Determine overall risk level
            if melanoma_risk < self.LOW_RISK_THRESHOLD:
                overall_risk = "low"
                recommendation = "Monitor lesion. Schedule routine dermatology check-up."
            elif melanoma_risk < self.HIGH_RISK_THRESHOLD:
                overall_risk = "medium"
                recommendation = "Dermatologist consultation recommended within 4 weeks."
            else:
                overall_risk = "high"
                recommendation = "Urgent dermatologist consultation recommended within 2 weeks."
            
            result = {
                "overall_risk": overall_risk,
                "melanoma_risk_score": round(melanoma_risk, 2),
                "risk_factors": risk_factors if risk_factors else ["No significant risk factors identified"],
                "protective_factors": protective_factors if protective_factors else [],
                "recommendation": recommendation
            }
            
            logger.info(f"Risk assessment: {overall_risk} (score: {melanoma_risk:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"Error in risk assessment: {e}")
            return {
                "overall_risk": "medium",
                "melanoma_risk_score": 0.5,
                "risk_factors": ["Unable to complete full risk assessment"],
                "protective_factors": [],
                "recommendation": "Consult with a dermatologist for proper evaluation."
            }


# Global predictor instance
_risk_predictor = None


def get_risk_predictor() -> RiskPredictor:
    """Get or create global risk predictor instance."""
    global _risk_predictor
    if _risk_predictor is None:
        _risk_predictor = RiskPredictor()
    return _risk_predictor
