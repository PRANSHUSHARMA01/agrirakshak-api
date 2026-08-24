import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Advisory(Base):
    __tablename__ = "advisories"

    id = Column(Integer, primary_key=True, index=True)
    farmer_case_id = Column(Integer, ForeignKey("farmer_cases.id"), nullable=True)
    diagnosis_or_answer = Column(Text, nullable=False)
    recommended_actions_json = Column(Text, nullable=True)  # JSON array of strings
    safety_notes_json = Column(Text, nullable=True)         # JSON array of strings
    escalation_flag = Column(Text, nullable=True)           # string or boolean store
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    farmer_case = relationship("FarmerCase", back_populates="advisories")
