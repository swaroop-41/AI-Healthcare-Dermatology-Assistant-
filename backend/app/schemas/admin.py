"""
Admin dashboard schemas.
"""

from pydantic import BaseModel
from typing import Dict, List, Any
from datetime import datetime


class SystemStats(BaseModel):
    """System overview statistics."""
    total_diagnoses: int
    total_patients: int
    total_users: int
    model_accuracy: float
    avg_confidence: float
    high_risk_cases: int


class ConditionStats(BaseModel):
    """Statistics by condition."""
    condition_counts: Dict[str, int]
    condition_percentages: Dict[str, float]


class ModelPerformance(BaseModel):
    """Model performance metrics."""
    precision_per_class: Dict[str, float]
    recall_per_class: Dict[str, float]
    f1_per_class: Dict[str, float]
    confusion_matrix: List[List[int]]
    overall_accuracy: float


class UserActivity(BaseModel):
    """User activity metrics."""
    active_users_today: int
    active_users_week: int
    active_users_month: int
    new_registrations_week: int
    avg_diagnoses_per_user: float


class SystemHealth(BaseModel):
    """System health status."""
    api_status: str
    database_status: str
    model_status: str
    avg_response_time_ms: float
    error_rate: float
    uptime_percentage: float
