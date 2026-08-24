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

    def predict_image(self, image_bytes: bytes, filename: str = "leaf.jpg") -> Dict[str, Any]:
        """
        Send image bytes to external POST /predict endpoint and return normalized output.
        """
        endpoint = f"{self.base_url}/predict"
        files = {"file": (filename, image_bytes, "image/jpeg")}

        try:
            resp = requests.post(endpoint, files=files, timeout=10.0)
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

                # If confidence is expressed as a percentage (e.g. 85.5), convert to 0-1 range
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
            else:
                return {
                    "success": False,
                    "error": f"External API returned HTTP status {resp.status_code}",
                    "fallback_message": "I couldn't process that image, please try again or describe the symptoms instead."
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Network/connection error calling prediction service: {str(e)}",
                "fallback_message": "I couldn't process that image, please try again or describe the symptoms instead."
            }

# Default instance
prediction_client = PredictionClient()
