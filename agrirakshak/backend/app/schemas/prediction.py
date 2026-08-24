from pydantic import BaseModel
from typing import Optional, Dict, Any

class PredictionResponse(BaseModel):
    success: bool
    predicted_class: str
    confidence: float
    needs_expert_review: bool
    raw_response: Dict[str, Any] = {}
    fallback_message: Optional[str] = None
