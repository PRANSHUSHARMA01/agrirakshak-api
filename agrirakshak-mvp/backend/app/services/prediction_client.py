import os
import requests
from typing import Dict, Any, Optional

PREDICTION_API_URL = os.getenv("PREDICTION_API_URL", "http://127.0.0.1:8000").rstrip("/")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.60"))

class PredictionClient:
    """
    Thin HTTP client wrapper for the external AgriRakshak prediction microservice.
    Normalizes prediction results and enforces expert review thresholding.
    """

    def __init__(self, base_url: Optional[str] = None, threshold: Optional[float] = None):
        self.base_url = (base_url or PREDICTION_API_URL).rstrip("/")
        self.threshold = threshold if threshold is not None else CONFIDENCE_THRESHOLD

    def check_health(self) -> bool:
        """
        Check whether the external prediction service is healthy.
        """
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("status") == "ok" or data.get("model_loaded") is True
            return False
        except Exception:
            return False

    def predict_with_gemini_vision(self, image_bytes: bytes) -> Optional[Dict[str, Any]]:
        """
        Runs cloud image inference using Gemini 2.0 Flash Vision API when external microservice is unavailable.
        """
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            return None

        try:
            import base64
            import json
            b64_img = base64.b64encode(image_bytes).decode("utf-8")

            prompt = (
                "You are an expert plant pathologist and AI crop disease diagnosis engine for AgriRakshak. "
                "Examine the provided image of the crop leaf carefully. "
                "Identify the crop type, disease/pest name (or if it is healthy), and give a confidence score. "
                "Format your output strictly as a JSON object with the following fields: "
                '{"is_crop_photo": true, "crop": "Rice", '
                '"predicted_class": "01_Bacterial_leaf_blight", '
                '"confidence": 0.94, "description": "Brief description of observed leaf symptoms"}'
            )

            models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash-latest", "gemini-flash-latest"]

            for model_name in models_to_try:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                    payload = {
                        "contents": [
                            {
                                "parts": [
                                    {"text": prompt},
                                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_img}}
                                ]
                            }
                        ],
                        "generationConfig": {"response_mime_type": "application/json", "temperature": 0.2}
                    }

                    resp = requests.post(url, json=payload, timeout=8.0)
                    if resp.status_code == 200:
                        res_data = resp.json()
                        candidates = res_data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts:
                                json_str = parts[0].get("text", "").strip()
                                parsed = json.loads(json_str)

                                raw_class = parsed.get("predicted_class", "01_Bacterial_leaf_blight")
                                confidence = float(parsed.get("confidence", 0.92))
                                conf_normalized = round(confidence, 4) if confidence <= 1.0 else round(confidence / 100.0, 4)
                                needs_expert = conf_normalized < self.threshold

                                return {
                                    "success": True,
                                    "predicted_class": raw_class,
                                    "confidence": conf_normalized,
                                    "needs_expert_review": needs_expert,
                                    "top_predictions": [],
                                    "raw_response": parsed
                                }
                except Exception:
                    pass
        except Exception:
            pass

        return None

    def predict_image(self, image_bytes: bytes, filename: str = "leaf.jpg") -> Dict[str, Any]:
        """
        Send image bytes to external POST /predict endpoint and return normalized output with Gemini Vision fallback.
        """
        endpoint = f"{self.base_url}/predict"
        files = {"file": (filename, image_bytes, "image/jpeg")}

        try:
            resp = requests.post(endpoint, files=files, timeout=5.0)
            if resp.status_code == 200:
                raw_data = resp.json()
                if not raw_data.get("success", False):
                    return {
                        "success": False,
                        "error": raw_data.get("error", "Prediction failed on external service."),
                        "fallback_message": "I couldn't process that image, please try again or describe the symptoms instead."
                    }

                predicted_class = raw_data.get("predicted_class") or raw_data.get("prediction", "Unknown")
                confidence = float(raw_data.get("confidence", 0.0))

                if confidence > 1.0:
                    conf_normalized = round(confidence / 100.0, 4)
                else:
                    conf_normalized = round(confidence, 4)

                needs_expert_review = conf_normalized < self.threshold

                return {
                    "success": True,
                    "predicted_class": predicted_class,
                    "confidence": conf_normalized,
                    "needs_expert_review": needs_expert_review,
                    "top_predictions": raw_data.get("top_predictions", []),
                    "raw_response": raw_data
                }
        except Exception:
            pass

        # Cloud Gemini Vision Fallback
        gemini_res = self.predict_with_gemini_vision(image_bytes)
        if gemini_res:
            return gemini_res

        return {
            "success": False,
            "error": "Network/connection error calling prediction service.",
            "fallback_message": "I couldn't process that image, please try again or describe the symptoms instead."
        }

# Default instance
prediction_client = PredictionClient()
