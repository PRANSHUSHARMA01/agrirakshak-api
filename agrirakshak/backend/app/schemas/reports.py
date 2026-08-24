import datetime
from pydantic import BaseModel
from typing import Optional, List, Any

class EscalationCreate(BaseModel):
    farmer_case_id: int
    reason: Optional[str] = "Low confidence prediction"

class EscalationResolve(BaseModel):
    expert_confirmed_diagnosis: str
    expert_notes: str

class FarmerCaseResponse(BaseModel):
    id: int
    session_id: str
    image_url: Optional[str] = None
    crop: str
    predicted_class: Optional[str] = None
    confidence: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_name: Optional[str] = None
    status: str
    needs_expert_review: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class EscalationResponse(BaseModel):
    id: int
    farmer_case_id: int
    reason: Optional[str] = None
    status: str
    expert_id: Optional[int] = None
    expert_diagnosis: Optional[str] = None
    expert_notes: Optional[str] = None
    created_at: datetime.datetime
    resolved_at: Optional[datetime.datetime] = None
    farmer_case: Optional[FarmerCaseResponse] = None

    class Config:
        from_attributes = True
