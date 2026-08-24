import re
from typing import Optional, Dict, Any

class IntentClassifier:
    """
    Intent classification service for AgriRakshak farmer chatbot.
    Routes queries into:
    - image_diagnosis
    - knowledge_query
    - weather_risk
    - general
    """

    WEATHER_KEYWORDS = ["weather", "rain", "temperature", "humidity", "monsoon", "rainfall", "forecast", "climate", "storm"]
    KNOWLEDGE_KEYWORDS = ["disease", "blight", "spot", "pest", "worm", "control", "spray", "pesticide", "fungicide", "symptom", "treatment", "dosage", "cure", "leaf", "rot", "smut"]
    AGRICULTURE_GENERAL_KEYWORDS = ["crop", "seed", "fertilizer", "irrigation", "soil", "harvest", "yield", "farming", "price", "mandi", "kisan", "scheme", "subsidy"]

    def classify(self, message: Optional[str] = None, has_image: bool = False, explicit_intent: Optional[str] = None) -> str:
        if explicit_intent in ["image_diagnosis", "knowledge_query", "weather_risk", "general"]:
            return explicit_intent

        if has_image:
            return "image_diagnosis"

        if not message:
            return "general"

        msg_lower = message.lower()

        # Check weather keywords
        if any(w in msg_lower for w in self.WEATHER_KEYWORDS):
            return "weather_risk"

        # Check knowledge base keywords
        if any(w in msg_lower for w in self.KNOWLEDGE_KEYWORDS):
            return "knowledge_query"

        # Check general agriculture keywords
        if any(w in msg_lower for w in self.AGRICULTURE_GENERAL_KEYWORDS):
            return "general"

        return "general"

intent_classifier = IntentClassifier()
