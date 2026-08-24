from fastapi import APIRouter
from app.services.prediction_client import prediction_client

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    pred_health = prediction_client.check_health()
    return {
        "status": "healthy",
        "service": "AgriRakshak Backend API",
        "prediction_service": pred_health
    }
