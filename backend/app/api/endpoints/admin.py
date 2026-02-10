"""
Admin dashboard endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from backend.app.db.base import get_db
from backend.app.db.models import User, Patient, Diagnosis, MedicalImage, DiagnosisStatus
from backend.app.schemas.admin import SystemStats, ConditionStats, ModelPerformance, UserActivity, SystemHealth
from backend.app.core.security import get_current_user, check_role
from backend.app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/stats/overview", response_model=SystemStats)
async def get_system_overview(
    current_user: dict = Depends(check_role("admin")),
    db: Session = Depends(get_db)
):
    """Get system overview statistics."""
    try:
        total_diagnoses = db.query(func.count(Diagnosis.id)).scalar()
        total_patients = db.query(func.count(Patient.id)).scalar()
        total_users = db.query(func.count(User.id)).scalar()
        
        # Calculate average confidence
        avg_confidence = db.query(func.avg(Diagnosis.confidence_score)).scalar() or 0.0
        
        # Count high risk cases
        high_risk_cases = db.query(func.count(Diagnosis.id)).filter(
            Diagnosis.risk_level == "high"
        ).scalar()
        
        # Model accuracy (placeholder - would come from validation set)
        model_accuracy = 0.86
        
        return {
            "total_diagnoses": total_diagnoses or 0,
            "total_patients": total_patients or 0,
            "total_users": total_users or 0,
            "model_accuracy": model_accuracy,
            "avg_confidence": round(avg_confidence, 2),
            "high_risk_cases": high_risk_cases or 0
        }
        
    except Exception as e:
        logger.error(f"Error getting system overview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system overview"
        )


@router.get("/stats/conditions", response_model=ConditionStats)
async def get_condition_statistics(
    current_user: dict = Depends(check_role("admin")),
    db: Session = Depends(get_db)
):
    """Get statistics by condition."""
    try:
        # Count diagnoses by condition
        condition_counts = db.query(
            Diagnosis.primary_prediction,
            func.count(Diagnosis.id).label('count')
        ).group_by(Diagnosis.primary_prediction).all()
        
        total = sum(count for _, count in condition_counts)
        
        counts_dict = {condition: count for condition, count in condition_counts}
        percentages_dict = {
            condition: round((count / total * 100), 2) if total > 0 else 0
            for condition, count in condition_counts
        }
        
        return {
            "condition_counts": counts_dict,
            "condition_percentages": percentages_dict
        }
        
    except Exception as e:
        logger.error(f"Error getting condition statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get condition statistics"
        )


@router.get("/stats/model", response_model=ModelPerformance)
async def get_model_performance(
    current_user: dict = Depends(check_role("admin")),
    db: Session = Depends(get_db)
):
    """Get model performance metrics."""
    try:
        # Placeholder values - in production, these would come from validation/test set
        # or from doctor-confirmed diagnoses vs AI predictions
        
        classes = ['AK', 'BCC', 'BKL', 'DF', 'MEL', 'NV', 'SCC', 'VASC']
        
        precision = {cls: 0.85 for cls in classes}
        recall = {cls: 0.82 for cls in classes}
        f1 = {cls: 0.83 for cls in classes}
        
        # Mock confusion matrix (8x8 for 8 classes)
        confusion_matrix = [
            [45, 2, 1, 0, 1, 0, 1, 0],
            [1, 52, 1, 0, 2, 1, 0, 0],
            [0, 1, 38, 1, 0, 2, 0, 0],
            [0, 0, 1, 25, 0, 1, 0, 0],
            [1, 1, 0, 0, 42, 2, 1, 0],
            [0, 2, 1, 1, 1, 85, 0, 1],
            [1, 0, 0, 0, 2, 0, 31, 0],
            [0, 0, 0, 0, 0, 1, 0, 22]
        ]
        
        return {
            "precision_per_class": precision,
            "recall_per_class": recall,
            "f1_per_class": f1,
            "confusion_matrix": confusion_matrix,
            "overall_accuracy": 0.86
        }
        
    except Exception as e:
        logger.error(f"Error getting model performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get model performance"
        )


@router.get("/stats/activity", response_model=UserActivity)
async def get_user_activity(
    current_user: dict = Depends(check_role("admin")),
    db: Session = Depends(get_db)
):
    """Get user activity metrics."""
    try:
        now = datetime.utcnow()
        day_ago = now - timedelta(days=1)
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # Active users (based on diagnosis creation as proxy for activity)
        active_today = db.query(func.count(func.distinct(Diagnosis.patient_id))).filter(
            Diagnosis.created_at >= day_ago
        ).scalar() or 0
        
        active_week = db.query(func.count(func.distinct(Diagnosis.patient_id))).filter(
            Diagnosis.created_at >= week_ago
        ).scalar() or 0
        
        active_month = db.query(func.count(func.distinct(Diagnosis.patient_id))).filter(
            Diagnosis.created_at >= month_ago
        ).scalar() or 0
        
        # New registrations
        new_registrations = db.query(func.count(User.id)).filter(
            User.created_at >= week_ago
        ).scalar() or 0
        
        # Average diagnoses per user
        total_users = db.query(func.count(Patient.id)).scalar() or 1
        total_diagnoses = db.query(func.count(Diagnosis.id)).scalar() or 0
        avg_diagnoses = total_diagnoses / total_users if total_users > 0 else 0
        
        return {
            "active_users_today": active_today,
            "active_users_week": active_week,
            "active_users_month": active_month,
            "new_registrations_week": new_registrations,
            "avg_diagnoses_per_user": round(avg_diagnoses, 2)
        }
        
    except Exception as e:
        logger.error(f"Error getting user activity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user activity"
        )


@router.get("/system/health", response_model=SystemHealth)
async def get_system_health(
    current_user: dict = Depends(check_role("admin")),
    db: Session = Depends(get_db)
):
    """Get system health status."""
    try:
        # Check database connection
        try:
            db.execute("SELECT 1")
            db_status = "healthy"
        except:
            db_status = "unhealthy"
        
        # Placeholder values - in production, these would be real metrics
        return {
            "api_status": "healthy",
            "database_status": db_status,
            "model_status": "healthy",
            "avg_response_time_ms": 245.5,
            "error_rate": 0.02,
            "uptime_percentage": 99.8
        }
        
    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system health"
        )
