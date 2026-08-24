import os
import requests
from typing import Dict, Any, Optional

PREDICTION_API_URL = os.getenv("PREDICTION_API_URL", "http://127.0.0.1:8000").rstrip("/")
PREDICTION_CONFIDENCE_THRESHOLD = float(os.getenv("PREDICTION_CONFIDENCE_THRESHOLD", "0.60"))

class PredictionClient:
    """
    Thin HTTP client wrapper for the existing AgriRakshak Keras/FastAPI prediction microservice.
    Reads openapi.json schemas, wraps POST /predict, normalizes results, and applies confidence thresholding.
    """

    def __init__(self, base_url: Optional[str] = None, threshold: Optional[float] = None):
        self.base_url = (base_url or PREDICTION_API_URL).rstrip("/")
        self.threshold = threshold if threshold is not None else PREDICTION_CONFIDENCE_THRESHOLD

    def get_openapi_spec(self) -> Dict[str, Any]:
        """
        Fetch openapi.json schema from external prediction microservice.
        """
        try:
            resp = requests.get(f"{self.base_url}/openapi.json", timeout=3.0)
            if resp.status_code == 200:
                return resp.json()
            return {}
        except Exception as e:
            print(f"Error fetching openapi.json: {e}")
            return {}

    def check_health(self) -> Dict[str, Any]:
        """
        Check health status of external prediction service.
        """
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=3.0)
            if resp.status_code == 200:
                return resp.json()
            return {"status": "unhealthy", "model_loaded": False}
        except Exception as e:
            return {"status": "unreachable", "error": str(e), "model_loaded": False}

    def predict_image(self, image_bytes: bytes, filename: str = "leaf.jpg") -> Dict[str, Any]:
        """
        Send image bytes to POST /predict using multipart/form-data with field 'file'.
        Returns normalized payload:
        {
            "predicted_class": str,
            "confidence": float,
            "raw_response": dict,
            "needs_expert_review": bool,
            "success": bool,
            "fallback_message": str (optional)
        }
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
                        "predicted_class": "Unknown",
                        "confidence": 0.0,
                        "needs_expert_review": True,
                        "raw_response": raw_data,
                        "fallback_message": "I couldn't process that image right now. Please try again or describe the symptoms."
                    }

                predicted_class = raw_data.get("predicted_class") or raw_data.get("prediction", "Unknown")
                confidence = float(raw_data.get("confidence", 0.0))

                # Normalize confidence to 0.0 - 1.0 float
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
                    "raw_response": raw_data
                }
            else:
                return {
                    "success": False,
                    "predicted_class": "Unknown",
                    "confidence": 0.0,
                    "needs_expert_review": True,
                    "raw_response": {"http_status": resp.status_code, "text": resp.text},
                    "fallback_message": "I couldn't process that image right now. Please try again or describe the symptoms."
                }
        except Exception as e:
            return {
                "success": False,
                "predicted_class": "Unknown",
                "confidence": 0.0,
                "needs_expert_review": True,
                "raw_response": {"error": str(e)},
                "fallback_message": "I couldn't process that image right now. Please try again or describe the symptoms."
            }

# Singleton instance
prediction_client = PredictionClient()
