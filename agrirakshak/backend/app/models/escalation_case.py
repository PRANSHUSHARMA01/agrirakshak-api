import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class EscalationCase(Base):
    __tablename__ = "escalation_cases"

    id = Column(Integer, primary_key=True, index=True)
    farmer_case_id = Column(Integer, ForeignKey("farmer_cases.id"), nullable=False)
    reason = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, under_review, resolved
    expert_id = Column(Integer, ForeignKey("experts.id"), nullable=True)
    expert_diagnosis = Column(String, nullable=True)
    expert_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    farmer_case = relationship("FarmerCase", back_populates="escalations")
    expert = relationship("Expert", back_populates="escalations")
