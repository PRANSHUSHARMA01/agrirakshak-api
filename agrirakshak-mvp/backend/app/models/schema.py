import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class FarmerCase(Base):
    __tablename__ = "farmer_cases"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True)
    image_url = Column(String(255), nullable=True)
    predicted_class = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)
    needs_expert_review = Column(Boolean, default=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    crop_type = Column(String(50), nullable=True)
    region = Column(String(100), nullable=True)
    user_query = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    escalations = relationship("EscalationCase", back_populates="farmer_case", cascade="all, delete-orphan")

class EscalationCase(Base):
    __tablename__ = "escalation_cases"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("farmer_cases.id"), nullable=False)
    status = Column(String(20), default="pending")  # pending | resolved
    expert_confirmed_class = Column(String(100), nullable=True)
    expert_notes = Column(Text, nullable=True)
    resolved_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    farmer_case = relationship("FarmerCase", back_populates="escalations")

class Expert(Base):
    __tablename__ = "experts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="officer")  # officer | admin

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(Integer, primary_key=True, index=True)
    disease_class = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    symptoms = Column(Text, nullable=True)
    chemical_control = Column(Text, nullable=True)
    biological_control = Column(Text, nullable=True)
    cultural_control = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
