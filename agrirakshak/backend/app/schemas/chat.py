from pydantic import BaseModel
from typing import List, Optional

class AdvisoryResponse(BaseModel):
    diagnosis_or_answer: str
    recommended_actions: List[str] = []
    safety_notes: List[str] = []
    escalation_flag: bool = False

class ChatMessageRequest(BaseModel):
    session_id: str
    message: Optional[str] = ""
    language: str = "en"  # en or hi
    image_base64: Optional[str] = None
    crop: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ChatMessageResponse(BaseModel):
    intent: str
    session_id: str
    advisory: AdvisoryResponse
    prediction_result: Optional[dict] = None
    weather_risk: Optional[dict] = None
    farmer_case_id: Optional[int] = None
