import re
from typing import Optional

def classify_intent(message: str, has_image: bool = False) -> str:
    """
    Classifies farmer input into 4 distinct intents:
    - image_diagnosis
    - knowledge_query
    - weather_risk
    - general
    """
    if has_image:
        return "image_diagnosis"

    msg_lower = (message or "").lower().strip()
    if not msg_lower:
        return "general"

    # Image intent keywords
    image_keywords = ["photo", "image", "tasveer", "picture", "dekho", "scan", "upload"]
    if any(k in msg_lower for k in image_keywords) and len(msg_lower.split()) < 6:
        return "image_diagnosis"

    # Weather intent keywords (English + Hindi/Hinglish)
    weather_keywords = ["mausam", "weather", "rain", "baarish", "barish", "forecast", "temperature", "humidity", "tapan", "garmi", "hawa", "wind"]
    if any(k in msg_lower for k in weather_keywords):
        return "weather_risk"

    # Knowledge query keywords (English + Hindi/Hinglish)
    knowledge_keywords = [
        "disease", "pest", "daag", "keeda", "keede", "kya hai", "control", "treatment",
        "upchar", "blast", "blight", "rust", "armyworm", "spot", "fertilizer", "pesticide",
        "irrigation", "syptoms", "lakshan", "rice", "maize", "chawal", "makka", "fasal",
        "patton", "leaf", "leaves", "yellow", "brown", "dry", "wilt", "rotting"
    ]
    if any(k in msg_lower for k in knowledge_keywords):
        return "knowledge_query"

    # Check for general agricultural question format
    if any(w in msg_lower for w in ["how", "what", "why", "when", "kaise", "kya", "kab", "kyun"]):
        return "knowledge_query"

    return "general"
