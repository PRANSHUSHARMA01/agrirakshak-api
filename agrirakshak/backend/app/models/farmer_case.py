import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base

class FarmerCase(Base):
    __tablename__ = "farmer_cases"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    image_url = Column(String, nullable=True)
    crop = Column(String, default="Unknown", index=True)
    predicted_class = Column(String, nullable=True)
    confidence = Column(Float, default=0.0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_name = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, diagnosed, escalated, resolved
    needs_expert_review = Column(Boolean, default=False)
    raw_prediction = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    escalations = relationship("EscalationCase", back_populates="farmer_case")
    advisories = relationship("Advisory", back_populates="farmer_case")
