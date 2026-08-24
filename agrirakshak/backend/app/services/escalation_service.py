import datetime
from sqlalchemy.orm import Session
from app.models.farmer_case import FarmerCase
from app.models.escalation_case import EscalationCase

def create_escalation(db: Session, farmer_case_id: int, reason: str = "Low confidence prediction") -> EscalationCase:
    """
    Creates an EscalationCase for expert review queue.
    """
    farmer_case = db.query(FarmerCase).filter(FarmerCase.id == farmer_case_id).first()
    if farmer_case:
        farmer_case.status = "escalated"
        farmer_case.needs_expert_review = True

    escalation = EscalationCase(
        farmer_case_id=farmer_case_id,
        reason=reason,
        status="pending",
        created_at=datetime.datetime.utcnow()
    )
    db.add(escalation)
    db.commit()
    db.refresh(escalation)
    return escalation
