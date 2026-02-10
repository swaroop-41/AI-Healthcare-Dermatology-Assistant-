"""
API router configuration.
"""

from fastapi import APIRouter
from backend.app.api.endpoints import auth, dermatology, patients, chatbot, reports, admin

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(dermatology.router, prefix="/dermatology", tags=["Dermatology Analysis"])
api_router.include_router(patients.router, prefix="/patients", tags=["Patient Management"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["AI Chatbot"])
api_router.include_router(reports.router, prefix="/reports", tags=["Report Generation"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin Dashboard"])
