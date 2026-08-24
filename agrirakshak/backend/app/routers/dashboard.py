from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.farmer_case import FarmerCase
from app.models.escalation_case import EscalationCase

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_cases = db.query(FarmerCase).count()
    today_cases = db.query(FarmerCase).filter(func.date(FarmerCase.created_at) == func.current_date()).count()
    pending_escalations = db.query(EscalationCase).filter(EscalationCase.status == "pending").count()
    high_risk_areas = 3  # Placeholder counter until weather/spatial scan

    return {
        "total_cases": total_cases,
        "today_cases": today_cases,
        "high_risk_areas": high_risk_areas,
        "pending_expert_reviews": pending_escalations
    }

@router.get("/cases")
def get_dashboard_cases(limit: int = 100, db: Session = Depends(get_db)):
    cases = db.query(FarmerCase).order_by(FarmerCase.created_at.desc()).limit(limit).all()
    return cases

@router.get("/diseases")
def get_disease_distribution(db: Session = Depends(get_db)):
    results = db.query(
        FarmerCase.predicted_class, func.count(FarmerCase.id)
    ).group_by(FarmerCase.predicted_class).all()

    return [{"disease": r[0] or "Unknown", "count": r[1]} for r in results]
