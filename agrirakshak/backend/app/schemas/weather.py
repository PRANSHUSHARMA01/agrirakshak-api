from pydantic import BaseModel
from typing import Optional, List

class WeatherRiskRequest(BaseModel):
    latitude: float
    longitude: float
    crop: Optional[str] = "Rice"
    sowing_date: Optional[str] = None

class WeatherRiskResponse(BaseModel):
    risk_level: str  # LOW, MEDIUM, HIGH
    reason: str
    recommended_actions: List[str]
    temperature_celsius: Optional[float] = None
    humidity_percent: Optional[float] = None
    weather_condition: Optional[str] = None
    forecast_3day_summary: Optional[str] = None
