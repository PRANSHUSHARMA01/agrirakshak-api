import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.farmer_case import FarmerCase
from app.models.escalation_case import EscalationCase
from app.schemas.reports import FarmerCaseResponse, EscalationResponse, EscalationResolve

router = APIRouter(prefix="/reports", tags=["Reports & Escalations"])

@router.get("", response_model=List[FarmerCaseResponse])
def get_reports(limit: int = 50, db: Session = Depends(get_db)):
    """
    Get recent farmer cases history.
    """
    cases = db.query(FarmerCase).order_by(FarmerCase.created_at.desc()).limit(limit).all()
    return cases

@router.get("/escalations", response_model=List[EscalationResponse])
def get_escalations(status: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """
    Get queue of escalated cases for expert review.
    """
    query = db.query(EscalationCase)
    if status:
        query = query.filter(EscalationCase.status == status)
    return query.order_by(EscalationCase.created_at.desc()).all()

@router.post("/escalations/{id}/resolve", response_model=EscalationResponse)
def resolve_escalation(id: int, payload: EscalationResolve, db: Session = Depends(get_db)):
    """
    Resolves an escalated case by recording confirmed diagnosis and expert advisory notes.
    """
    escalation = db.query(EscalationCase).filter(EscalationCase.id == id).first()
    if not escalation:
        raise HTTPException(status_code=404, detail="Escalation case not found.")

    now = datetime.datetime.utcnow()
    escalation.expert_diagnosis = payload.expert_confirmed_diagnosis
    escalation.expert_notes = payload.expert_notes
    escalation.status = "resolved"
    escalation.resolved_at = now

    # Update linked FarmerCase status & expert confirmed diagnosis
    if escalation.farmer_case:
        escalation.farmer_case.status = "resolved"
        escalation.farmer_case.predicted_class = f"[Confirmed] {payload.expert_confirmed_diagnosis}"

    db.commit()
    db.refresh(escalation)
    return escalation
