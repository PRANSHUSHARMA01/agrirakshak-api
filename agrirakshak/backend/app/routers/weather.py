from fastapi import APIRouter, Query
from typing import Optional
from app.services.weather_service import evaluate_weather_risk
from app.schemas.weather import WeatherRiskResponse

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/risk", response_model=WeatherRiskResponse)
def get_weather_risk(
    latitude: float = Query(28.6139, description="Latitude coordinate"),
    longitude: float = Query(77.2090, description="Longitude coordinate"),
    crop: str = Query("Rice", description="Target crop name"),
    sowing_date: Optional[str] = Query(None, description="Optional sowing date YYYY-MM-DD")
):
    """
    Evaluates real-time weather and 3-day forecast to issue crop disease risk alerts.
    """
    return evaluate_weather_risk(lat=latitude, lon=longitude, crop=crop, sowing_date=sowing_date)
