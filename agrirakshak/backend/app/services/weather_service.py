import requests
from typing import Dict, Any, Optional
from app.config import settings
from app.schemas.weather import WeatherRiskResponse

# Default Risk Rules Configuration
RISK_RULES = {
    "fungal_high": {
        "humidity_min": 80,
        "temperature_min": 20,
        "temperature_max": 30
    },
    "fungal_medium": {
        "humidity_min": 65,
        "temperature_min": 18,
        "temperature_max": 32
    },
    "pest_high": {
        "temperature_min": 32,
        "humidity_max": 60
    }
}

def fetch_openweather_data(lat: float, lon: float) -> Dict[str, Any]:
    """
    Fetches real-time weather and forecast data from OpenWeatherMap API.
    Falls back to realistic synthetic data if API key is unconfigured or call fails.
    """
    api_key = settings.OPENWEATHER_API_KEY
    if not api_key:
        return get_mock_weather_data(lat, lon)

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        resp = requests.get(url, timeout=4.0)
        if resp.status_code == 200:
            data = resp.json()
            main = data.get("main", {})
            weather_desc = data.get("weather", [{}])[0].get("main", "Clear")
            wind_speed = data.get("wind", {}).get("speed", 0.0)

            # Try fetching 3-day forecast
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            f_resp = requests.get(forecast_url, timeout=4.0)
            forecast_summary = "Expect moderate weather condition over next 3 days."
            if f_resp.status_code == 200:
                f_data = f_resp.json()
                list_items = f_data.get("list", [])[:8]  # next 24-48 hrs
                rain_count = sum(1 for item in list_items if "Rain" in item.get("weather", [{}])[0].get("main", ""))
                if rain_count > 2:
                    forecast_summary = "High probability of rain and high humidity over next 3 days."
                else:
                    forecast_summary = "Fair weather with occasional cloud cover over next 3 days."

            return {
                "temp": main.get("temp", 28.0),
                "humidity": main.get("humidity", 82.0),
                "condition": weather_desc,
                "wind_speed": wind_speed,
                "forecast_summary": forecast_summary,
                "is_real": True
            }
        else:
            return get_mock_weather_data(lat, lon)
    except Exception as e:
        print(f"OpenWeatherMap fetch error: {e}")
        return get_mock_weather_data(lat, lon)

def get_mock_weather_data(lat: float, lon: float) -> Dict[str, Any]:
    """
    Realistic demo weather provider for offline testing and hackathon demonstration.
    """
    # Deterministic mock generation based on lat/lon
    simulated_temp = round(25.0 + (abs(lat) % 8), 1)
    simulated_humidity = round(75.0 + (abs(lon) % 18), 1)
    if simulated_humidity > 90:
        simulated_humidity = 88.0

    return {
        "temp": simulated_temp,
        "humidity": simulated_humidity,
        "condition": "Humid / Partly Cloudy",
        "wind_speed": 12.5,
        "forecast_summary": "High relative humidity (82-88%) and cloudy skies forecasted for next 72 hours.",
        "is_real": False
    }

def evaluate_weather_risk(lat: float, lon: float, crop: str = "Rice", sowing_date: Optional[str] = None) -> WeatherRiskResponse:
    """
    Evaluates weather data against agricultural risk rules for crop fungal/pest outbreaks.
    """
    w_data = fetch_openweather_data(lat, lon)
    temp = w_data["temp"]
    humidity = w_data["humidity"]
    condition = w_data["condition"]
    forecast = w_data["forecast_summary"]

    risk_level = "LOW"
    reason = f"Weather parameters for {crop} are within standard seasonal thresholds (Temp: {temp}°C, Humidity: {humidity}%)."
    actions = [
        "Continue normal field irrigation and weekly crop monitoring.",
        "Ensure field bunds are clean of weeds."
    ]

    # Evaluate Fungal High Risk
    f_high = RISK_RULES["fungal_high"]
    f_med = RISK_RULES["fungal_medium"]

    if humidity >= f_high["humidity_min"] and f_high["temperature_min"] <= temp <= f_high["temperature_max"]:
        risk_level = "HIGH"
        reason = f"High humidity ({humidity}%) combined with favorable temperatures ({temp}°C) creates a critical risk zone for fungal diseases such as Rice Blast, Sheath Blight, or Leaf Spot."
        actions = [
            "Inspect leaves regularly every morning for water-soaked lesions.",
            "Avoid overhead leaf wetness; pause evening irrigation.",
            "Do not apply excessive nitrogen fertilizer during this high-humidity window.",
            "Keep recommended bio-fungicides (e.g. Trichoderma or Pseudomonas) ready."
        ]
    elif humidity >= f_med["humidity_min"] and f_med["temperature_min"] <= temp <= f_med["temperature_max"]:
        risk_level = "MEDIUM"
        reason = f"Moderate humidity ({humidity}%) and temperature ({temp}°C) indicate elevated risk for bacterial and fungal leaf infections."
        actions = [
            "Monitor crop canopy for early spot symptoms.",
            "Ensure proper field drainage after rainfall.",
            "Maintain clean field borders to reduce spore accumulation."
        ]

    return WeatherRiskResponse(
        risk_level=risk_level,
        reason=reason,
        recommended_actions=actions,
        temperature_celsius=temp,
        humidity_percent=humidity,
        weather_condition=condition,
        forecast_3day_summary=forecast
    )
